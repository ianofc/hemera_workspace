import asyncio
import logging
import os
import time
from typing import Dict

logger = logging.getLogger("SARA_VIGILANCE")

# Tenta importar psutil para monitoramento real de recursos
try:
    import psutil
except ImportError:
    psutil = None


class SaraVigilanceDaemon:
    def __init__(self):
        self.state = "SLEEP"  # SLEEP, NORMAL ou WAKE
        self.request_count = 0
        self.event_count = 0
        self.total_latency = 0.0
        self.last_check_time = time.time()
        self.running = False
        self._task = None

        # Carrega limites iniciais das variáveis de ambiente para conformidade de testes
        thalamus_default = self._budget_from_env("TAS_BUDGET_THALAMUS_MS", 15)
        sara_default = self._budget_from_env("TAS_BUDGET_SARA_MS", 45)
        accumbens_default = self._budget_from_env("TAS_BUDGET_ACCUMBENS_MS", 25)

        # Definição dos budgets dinâmicos (ms) para cada estado
        self.budgets = {
            "SLEEP": {
                "thalamus": max(1, thalamus_default * 2 // 3),
                "sara": max(1, sara_default * 2 // 3),
                "accumbens": max(1, accumbens_default * 2 // 3),
            },
            "NORMAL": {
                "thalamus": thalamus_default,
                "sara": sara_default,
                "accumbens": accumbens_default,
            },
            "WAKE": {
                "thalamus": max(1, thalamus_default // 2),
                "sara": max(1, sara_default // 2),
                "accumbens": max(1, accumbens_default // 2),
            }
        }

        # Budgets ativos padrão
        self.current_budgets = self.budgets["NORMAL"].copy()
        
        # Estatísticas acumuladas
        self.rps = 0.0
        self.eps = 0.0
        self.avg_latency_ms = 0.0
        self.cpu_percent = 0.0
        self.memory_percent = 0.0
        self.hpa_replicas = 1
        self.scale_up_needed = False

    @staticmethod
    def _budget_from_env(env_name: str, default: int) -> int:
        raw_value = os.getenv(env_name)
        try:
            parsed = int(raw_value) if raw_value is not None else default
        except (TypeError, ValueError):
            return default
        return max(parsed, 1)

    def record_request(self, latency_ms: float):
        self.request_count += 1
        self.total_latency += latency_ms

    def record_event(self):
        self.event_count += 1

    async def start(self):
        self.running = True
        self.last_check_time = time.time()
        self._task = asyncio.create_task(self._loop())
        logger.info("👁️ [SARA] Daemon de Vigília e Orquestração iniciado.")

    async def stop(self):
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 [SARA] Daemon de Vigília desligado.")

    async def _loop(self):
        while self.running:
            try:
                await asyncio.sleep(5)
                self.evaluate_system_state()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ [SARA] Erro no loop de vigília: {e}")

    def evaluate_system_state(self):
        now = time.time()
        elapsed = now - self.last_check_time
        if elapsed <= 0:
            elapsed = 5.0

        # Calcula taxas
        self.rps = round(self.request_count / elapsed, 2)
        self.eps = round(self.event_count / elapsed, 2)
        self.avg_latency_ms = round((self.total_latency / self.request_count) if self.request_count > 0 else 0.0, 2)

        # Reseta acumuladores para a próxima janela
        self.request_count = 0
        self.total_latency = 0.0
        self.event_count = 0
        self.last_check_time = now

        # Monitoramento de hardware
        if psutil:
            try:
                self.cpu_percent = psutil.cpu_percent(interval=None)
                self.memory_percent = psutil.virtual_memory().percent
            except Exception:
                self.cpu_percent = 15.0
                self.memory_percent = 40.0
        else:
            # Simulação caso psutil não esteja instalado
            self.cpu_percent = round(10.0 + (self.rps * 3.0), 2)
            self.memory_percent = 45.0

        # Tamanho da fila assíncrona do Talamus
        from app.engines.thalamus.queue import talamus_queue
        queue_size = talamus_queue.queue.qsize()

        # Lógica de Transição de Estado (Vigília)
        # Se CPU alta, latência alta ou fila congestionada, acorda em WAKE
        if self.rps > 10.0 or self.avg_latency_ms > 35.0 or queue_size > 30 or self.cpu_percent > 75.0:
            self.state = "WAKE"
            self.scale_up_needed = True
            self.hpa_replicas = min(5, max(3, int(self.rps / 5.0)))
            self.current_budgets = self.budgets["WAKE"].copy()
            logger.warning(
                f"🚨 [SARA WAKE] Estado de ALERTA ativado! RPS={self.rps}, Latência={self.avg_latency_ms}ms, "
                f"Fila={queue_size}, CPU={self.cpu_percent}%. Solicitando HPA ({self.hpa_replicas} réplicas). "
                f"Budgets ajustados para tempo de resposta crítico."
            )
        elif self.rps < 1.0 and queue_size == 0 and self.cpu_percent < 30.0:
            self.state = "SLEEP"
            self.scale_up_needed = False
            self.hpa_replicas = 1
            self.current_budgets = self.budgets["SLEEP"].copy()
        else:
            self.state = "NORMAL"
            self.scale_up_needed = False
            self.hpa_replicas = 1
            self.current_budgets = self.budgets["NORMAL"].copy()

    def get_status(self) -> Dict:
        from app.engines.thalamus.queue import talamus_queue
        return {
            "state": self.state,
            "rps": self.rps,
            "eps": self.eps,
            "avg_latency_ms": self.avg_latency_ms,
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "talamus_queue_size": talamus_queue.queue.qsize(),
            "hpa": {
                "scale_up_needed": self.scale_up_needed,
                "recommended_replicas": self.hpa_replicas,
            },
            "active_budgets_ms": self.current_budgets,
        }


sara_vigilance = SaraVigilanceDaemon()
