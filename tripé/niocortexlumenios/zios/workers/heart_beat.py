import sys
import os
import asyncio

# Injeção Automática de Path: Resolve o erro de módulo no Windows
# Adiciona o diretório pai (raiz do ZIOS) ao path do sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.zios import ZiosOrchestrator
from core.resonance import ResonanceEngine

async def life_cycle():
    """O loop 'The Sims' que mantém o Zios acordado e atento."""
    zios = ZiosOrchestrator("ian_master")
    engine = ResonanceEngine()
    
    print("💓 ZIOS: Ciclo de vida iniciado. Onipresença ativa.")
    
    while True:
        # Simulação de percepção proativa (Urgência baseada no motor de ressonância)
        context = {"urgency": 0.9, "trigger": "heartbeat_pulse"}
        
        if engine.should_intervene(context):
            print("🔔 [RESSONÂNCIA]: Zios detectou necessidade de ação proativa.")
            # O Zios processa sem intervenção humana direta
            zios.process("Realizar varredura de integridade e logs prioritários.", context)
            
        await asyncio.sleep(60)

if __name__ == "__main__":
    try:
        asyncio.run(life_cycle())
    except KeyboardInterrupt:
        print("\n🛑 ZIOS: Batimento cardíaco encerrado.")