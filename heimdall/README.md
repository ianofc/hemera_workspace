# Heimdall

`heimdall` é a fundação de segurança do ecossistema Lyv. Ele foi desenhado para ser reutilizável entre projetos, cobrindo:

- login/registro (validação de senha e token);
- controle de IP e listas de bloqueio;
- defesa de endpoints e APIs (rate limit + políticas);
- trilha de auditoria com mascaramento de dados sensíveis;
- telemetria de saúde de segurança.

## Estrutura

- `config.py`: políticas centrais de segurança.
- `auth.py`: validação de senha e hash seguro de token.
- `network.py`: extração de IP real e apoio para análise de rede.
- `threats.py`: decisão de risco por IP/faixa.
- `rate_limit.py`: rate limiter de janela deslizante.
- `integrity.py`: guarda de integridade de endpoint.
- `audit.py`: log de eventos com redação de dados sensíveis.
- `middleware.py`: middleware plugável em FastAPI/Starlette.
- `integration.py`: bootstrap de integração por variáveis de ambiente.
- `health.py`: payload de status de segurança.

## Exemplo rápido (FastAPI)

```python
from fastapi import FastAPI
from heimdall import attach_heimdall

app = FastAPI()
attach_heimdall(app, service_name="meu-servico")
```

## Integração no projeto Lyv

Serviços já integrados para usar Heimdall por padrão:

- `fastapi_service/main.py`
- `tas/app/main.py`
- `zios/main.py`

## Variáveis de ambiente

- `HEIMDALL_ENABLED` (`true`/`false`) - ativa/desativa middleware.
- `HEIMDALL_BLOCKED_NETWORKS` (csv CIDR) - ex: `10.0.0.0/8,192.168.0.0/16`
- `HEIMDALL_TRUSTED_PROXIES` (csv IPs)
- `HEIMDALL_SENSITIVE_FIELDS` (csv campos para mascarar)
- `HEIMDALL_RATE_LIMIT_REQUESTS` (int)
- `HEIMDALL_RATE_LIMIT_WINDOW_SECONDS` (int)

## Princípios

1. **Secure-by-default**: regras mais rígidas por padrão.
2. **Observabilidade**: tudo que for evento de segurança deve ser auditável.
3. **Extensibilidade**: qualquer projeto pode sobrescrever políticas sem reescrever a base.
4. **Privacidade**: mascaramento de campos sensíveis nos logs.
