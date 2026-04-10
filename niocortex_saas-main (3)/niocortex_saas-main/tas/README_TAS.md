# TAS ENGINE - DOCUMENTAÇÃO TÉCNICA v1.0
Gerado em: 2026-01-15 04:49:57

## 1. Arquitetura (Trindade TAS)
- **Thalamus (O Porteiro):** Responsável pela soberania do utilizador e filtros legais. Executa o veto antes de qualquer cálculo pesado. [cite: 39]
- **SARA (A Atenção):** Motor de busca semântica e afinidade vetorial utilizando similaridade de cosseno. [cite: 35, 38]
- **Accumbens (A Recompensa):** Algoritmo de ranking baseado em "Scores de Dopamina" (Share, Like, Click). [cite: 38]

## 2. Fluxo de Dados
1. Ingestão via `/api/v1/events/ingest` (Geração de Embeddings automática).
2. Armazenamento no Supabase (PostgreSQL + PgVector). [cite: 37]
3. Recomendação via `/api/v1/recommend/` (T -> S -> A).
4. Busca Semântica via `/api/v1/search/` (Vibe-based search).

## 3. Comandos de Manutenção
- **Iniciar Servidor (Dev):** python run_tas.py
- **Iniciar Servidor (Prod):** sh scripts/deploy_start.sh
- **Monitorizar Dopamina:** python scripts/monitor_dopamine.py
- **Sincronizar Banco:** python scripts/init_db.py

## 4. Variáveis de Ambiente (.env)
- DATABASE_URL: Conexão com Supabase. [cite: 1]
- API_V1_STR: Prefixo da API. [cite: 1]