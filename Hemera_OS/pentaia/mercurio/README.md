# 🛰️ Mercurio (Hub de Distribuição PentaIA)

**Mercurio** é o serviço de ponte e distribuição de dados em tempo real do ecossistema BIRD/PentaIA. Ele atua como um hub centralizado para geração de pacotes dinâmicos (bundles) e roteamento de informações entre microsserviços (ZIOS, TAS, IRIS, Backend) e clientes finais.

O nome Mercurio faz referência ao mensageiro dos deuses, refletindo a função de garantir que cada nó do sistema receba atualizações com baixa latência e tolerância a falhas.

## 🚀 Principais Funcionalidades

- **Geração de Bundles Dinâmicos**: consolida dados de múltiplas fontes para entrega otimizada com fallback automático.
- **Ponte de Comunicação (Bridge)**: interoperabilidade entre os nós de IA e segurança.
- **Broadcasting em Tempo Real (base)**: base para distribuição de eventos críticos.
- **Integração com Heimdall**: consulta de integridade por IP para enriquecer o contexto de segurança da resposta.

## 🛠️ Tecnologias Utilizadas

- **FastAPI**
- **Python 3.11+**
- **Requests**
- **Logging**
- **Docker**

---

## 🏗️ Estrutura do Projeto

```text
mercurio/
├── core/
│   ├── bridge.py       # Lógica de intermediação de dados
│   ├── broadcaster.py  # Base de gerenciamento de envios/eventos
│   └── config.py       # Variáveis de ambiente e constantes
├── main.py             # Ponto de entrada da aplicação FastAPI
├── Dockerfile          # Configuração de containerização
├── requirements.txt    # Dependências do projeto
└── README.md
```

---

## 🔌 Contrato da API

### `GET /api/v1/mercurio/bundle`
Retorna payload unificado para frontend:

- `trends[]`: lista normalizada (`id`, `category`, `topic`, `hashtag`, `volume`, `link`)
- `security`: status de segurança (com fallback local)
- `events[]`: eventos operacionais
- `news[]`: notícias complementares (quando disponíveis)
- `metadata`: origem dos dados e timestamp de geração

### `GET /`
Healthcheck do nó Mercurio.

---

## 🚦 Roadmap de Desenvolvimento

### Fase 1: Fundação (Concluída/Atual)

- [x] API base com FastAPI.
- [x] Endpoint `/api/v1/mercurio/bundle`.
- [x] Logs de operação.
- [x] Dockerização.
- [x] Fallback TAS -> IRIS -> FALLBACK.
- [x] Normalização de schema para consumo frontend.

### Fase 2: Performance e Distribuição (Próximos Passos)

- [ ] **Caching de Bundles** com Redis.
- [ ] **WebSockets Nativos** para broadcast full-duplex.
- [ ] **Priorização de Tráfego** por tipo de evento.

### Fase 3: Inteligência e Segurança Avançada

- [ ] **Integração Profunda com Heimdall** para bloqueio automático.
- [ ] **Auto-Healing** para redirecionamento quando serviços vizinhos estiverem offline.
- [ ] **Compressão Adaptativa** de payload por perfil de conexão.

---

## 🔧 Como Executar

### Via Docker Compose (recomendado)

Na raiz do projeto:

```bash
docker compose up --build mercurio
```

### Localmente

1. Instale as dependências:

```bash
pip install -r mercurio/requirements.txt
```

2. Execute o servidor:

```bash
cd mercurio
uvicorn main:app --host 0.0.0.0 --port 8004 --reload
```

---

## ⚙️ Variáveis de Ambiente

- `MERCURIO_PORT` (default: `8004`)
- `MERCURIO_TIMEOUT` (default: `2.5`)
- `TAS_TRENDS_URL` (default: `http://tas:8001/api/v1/recommend/trends`)
- `IRIS_SCAN_URL` (default: `http://iris:8003/scan/full`)
- `HEIMDALL_CHECK_URL` (default: `http://zios:8002/v1/proactive/heimdall/check`)
- `MERCURIO_CORS_ALLOW_ORIGINS` (CSV, default: `http://localhost:8080,http://127.0.0.1:8080`)

---

## 📄 Licença

Uso exclusivo do grupo **IO Santos Group** e do ecossistema **BIRD**. Todos os direitos reservados.
