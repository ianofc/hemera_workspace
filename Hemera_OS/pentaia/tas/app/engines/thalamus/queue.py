import asyncio
import json
import logging
import os
from typing import Any, Callable, Dict, List

logger = logging.getLogger("TALAMUS_QUEUE")

# Variáveis de ambiente de configuração
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")


class TalamusEventQueue:
    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._worker_task = None
        self._handlers: List[Callable[[Dict[str, Any]], Any]] = []
        
        # Conexões opcionais externas
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
        self.kafka_producer = None

    def register_handler(self, handler: Callable[[Dict[str, Any]], Any]):
        self._handlers.append(handler)

    async def start(self):
        self._running = True
        
        # Tenta inicializar brokers externos se configurados
        if RABBITMQ_URL:
            await self._connect_rabbitmq()
        elif KAFKA_BOOTSTRAP_SERVERS:
            await self._connect_kafka()

        # Inicia o worker local do event loop
        self._worker_task = asyncio.create_task(self._worker())
        logger.info("🔌 [TALAMUS] Fila de eventos assíncrona iniciada com sucesso.")

    async def stop(self):
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        
        # Fecha conexões externas
        if self.rabbitmq_channel:
            try:
                self.rabbitmq_channel.close()
            except Exception:
                pass
        if self.rabbitmq_connection:
            try:
                self.rabbitmq_connection.close()
            except Exception:
                pass
        if self.kafka_producer:
            try:
                self.kafka_producer.close()
            except Exception:
                pass

        logger.info("🛑 [TALAMUS] Fila de eventos parada.")

    async def publish(self, event: Dict[str, Any]):
        """Publica o evento na fila local e propaga para o broker externo se ativo"""
        # Sanitiza o evento usando o sanitizador
        from app.engines.thalamus.ingress import thalamus_ingress
        sanitized_event = thalamus_ingress.sanitize_event_payload(event)

        # Enfileira localmente
        await self.queue.put(sanitized_event)
        
        # Registra a atividade de evento na SARA
        from app.engines.sara.vigilance import sara_vigilance
        sara_vigilance.record_event()

        # Envia para broker externo de forma não-bloqueante
        if self.rabbitmq_channel:
            try:
                self.rabbitmq_channel.basic_publish(
                    exchange='',
                    routing_key='tas_events',
                    body=json.dumps(sanitized_event)
                )
            except Exception as e:
                logger.warning(f"⚠️ [TALAMUS] Erro ao publicar no RabbitMQ, usando fila em memória: {e}")
        elif self.kafka_producer:
            try:
                self.kafka_producer.send(
                    'tas_events',
                    value=json.dumps(sanitized_event).encode('utf-8')
                )
            except Exception as e:
                logger.warning(f"⚠️ [TALAMUS] Erro ao publicar no Kafka, usando fila em memória: {e}")

    async def _worker(self):
        while self._running:
            try:
                event = await self.queue.get()
                
                # Executa todos os handlers registrados
                for handler in self._handlers:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(event)
                        else:
                            handler(event)
                    except Exception as e:
                        logger.error(f"❌ [TALAMUS] Erro no handler de evento: {e}")
                
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ [TALAMUS] Erro no worker loop da fila: {e}")
                await asyncio.sleep(1)

    async def _connect_rabbitmq(self):
        try:
            import pika
            # Executa a conexão síncrona do pika no loop de thread executor
            def do_connect():
                params = pika.URLParameters(RABBITMQ_URL)
                conn = pika.BlockingConnection(params)
                chan = conn.channel()
                chan.queue_declare(queue='tas_events', durable=True)
                return conn, chan

            loop = asyncio.get_event_loop()
            self.rabbitmq_connection, self.rabbitmq_channel = await loop.run_in_executor(None, do_connect)
            logger.info("📡 [TALAMUS] Conectado com sucesso ao RabbitMQ.")
        except Exception as e:
            logger.warning(f"⚠️ [TALAMUS] Falha ao conectar ao RabbitMQ ({e}). Usando modo Fallback local.")

    async def _connect_kafka(self):
        try:
            from kafka import KafkaProducer
            def do_connect():
                return KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","))

            loop = asyncio.get_event_loop()
            self.kafka_producer = await loop.run_in_executor(None, do_connect)
            logger.info("📡 [TALAMUS] Conectado com sucesso ao Kafka.")
        except Exception as e:
            logger.warning(f"⚠️ [TALAMUS] Falha ao conectar ao Kafka ({e}). Usando modo Fallback local.")


talamus_queue = TalamusEventQueue()
