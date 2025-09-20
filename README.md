# SensorFlow

[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-blue)](https://fastapi.tiangolo.com/)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen)](https://github.com/jpaullopes/sensorflow-server-ethernet)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Backend FastAPI para monitoramento de processos CIP (Clean-in-Place) com streaming em tempo real de dados de temperatura, pressão, concentração e fluxo via REST e WebSocket, compatível com WiFi e módulos Ethernet (W5500/W5100).

---

## Funcionalidades

### Core Features
- **API REST Segura**: Endpoints protegidos por API Key para recepção de dados de monitoramento CIP
- **WebSocket em Tempo Real**: Distribuição instantânea de dados CIP para clientes conectados
- **Armazenamento em Memória**: Dados mais recentes mantidos em memória para consulta rápida

### Arquitetura Moderna
- **Clean Architecture**: Separação clara entre domínio, aplicação e infraestrutura
- **Injeção de Dependências**: Desacoplamento entre componentes
- **Configuração Externa**: Variáveis de ambiente para todas as configurações
- **Logs Estruturados**: Sistema avançado com níveis e formatação colorida

### Segurança & Performance  
- **Autenticação Dupla**: API Keys independentes para HTTP e WebSocket
- **Limitação de Conexões**: Controle granular de conexões por API Key
- **Validação de Dados**: Schemas Pydantic para validação automática

### DevOps & Deployment
- **Docker Compose**: Stack simplificada com orquestração de serviços
- **Healthchecks**: Verificação automática de saúde dos containers
- **Compatibilidade Ethernet**: Suporte nativo para módulos W5500 e W5100

## Tecnologias

### Backend & Framework
- **Python**: 3.11+
- **FastAPI**: Framework moderno e rápido com documentação automática
- **Uvicorn**: Servidor ASGI de alta performance
- **Pydantic**: Validação de dados e serialização

### Comunicação & Real-time
- **WebSocket**: Streaming bidirecional para dados em tempo real
- **Server-Sent Events**: Alternativa unidirecional para push de dados

### Containerização & Orquestração
- **Docker**: Containerização da aplicação
- **Docker Compose**: Orquestração simplificada de serviços

### Observabilidade & Logging
- **ColorLog**: Logs coloridos e estruturados
- **FastAPI Logging**: Integração nativa para traces de requisições

---

## Quick Start

### Pré-requisitos

- **Docker & Docker Compose**: [Instalar Docker](https://docs.docker.com/get-docker/)
- **Git**: Para clonar o repositório

### Instalação e Execução

1. **Clone o repositório**
```bash
git clone https://github.com/jpaullopes/sensorflow-server-ethernet.git
cd sensorflow-server-ethernet
```

2. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. **Execute com Docker Compose**
```bash
docker-compose up -d
```

4. **Acesse os serviços**

| Serviço    | URL                                        | Credenciais      |
|------------|--------------------------------------------|------------------|
| **API**    | [http://localhost:8000](http://localhost:8000) | API Key via header |
| **Docs**   | [http://localhost:8000/docs](http://localhost:8000/docs) | Interface Swagger |

### Comandos Úteis

```bash
# Rebuild a API (após mudanças no código)
docker-compose up --build -d api

# Verificar logs
docker-compose logs api

# Parar o serviço
docker-compose down
```

## API Endpoints

### Recepção de Dados dos Sensores

**POST** `/sensor_data`

Envia dados dos sensores CIP para o sistema.

```bash
curl -X POST "http://localhost:8000/sensor_data" \
  -H "X-API-Key: sua_chave_api" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 75.5,
    "pressure": 2.3,
    "concentration": 0.8,
    "flow": 1.2
  }'
```

### Consulta de Dados Mais Recentes

**GET** `/sensor_data`

Retorna os dados mais recentes recebidos pelos sensores.

```bash
curl -X GET "http://localhost:8000/sensor_data"
```

### Health Check

**GET** `/health`

Verifica a saúde da API.

```bash
curl -X GET "http://localhost:8000/health"
```

### WebSocket para Dados em Tempo Real

**WebSocket** `/sensor_updates?api-key=sua_chave_ws`

Conecta via WebSocket para receber dados em tempo real conforme são enviados pelos sensores.

```javascript
const ws = new WebSocket('ws://localhost:8000/sensor_updates?api-key=sua_chave_ws');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Dados recebidos:', data);
};
```

## Configuração

### Variáveis de Ambiente

```bash
# Configurações de API
API_KEY=your_api_key_here
API_KEY_WS=your_websocket_api_key_here

# WebSocket Configuration
MAX_WS_CONNECTIONS_PER_KEY=10
```

### Estrutura do Payload

**Dados dos Sensores**:
```json
{
  "temperature": 75.5,
  "pressure": 2.3,
  "concentration": 0.8,
  "flow": 1.2
}
```

**Resposta da API**:
```json
{
  "temperature": 75.5,
  "pressure": 2.3,
  "concentration": 0.8,
  "flow": 1.2,
  "timestamp": "2024-01-15T10:30:00-03:00",
  "cip_id": 1
}
```

## Desenvolvimento

### Executar Localmente

1. **Instalar dependências**
```bash
pip install -r requirements.txt
```

2. **Executar a aplicação**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Estrutura do Projeto

```
├── app/                     # Configuração principal da aplicação
├── src/                     # Código fonte
│   ├── api/                 # Endpoints e schemas
│   │   ├── routers/         # Rotas da API
│   │   └── schemas/         # Modelos Pydantic
│   └── infrastructure/      # Camada de infraestrutura
│       ├── config/          # Configurações
│       ├── logging/         # Sistema de logs
│       ├── security/        # Autenticação
│       └── websocket/       # Gerenciamento WebSocket
├── docker-compose.yml       # Orquestração Docker
├── Dockerfile              # Imagem da aplicação
└── requirements.txt        # Dependências Python
```

### Logs

A aplicação possui logs estruturados com diferentes níveis:

```bash
# Visualizar logs em tempo real
docker-compose logs -f api
```

## Hardware Compatível

### Módulos Ethernet Suportados
- **W5500**: Módulo Ethernet com SPI
- **W5100**: Módulo Ethernet básico
- **ESP32 com Ethernet**: Placas com PHY integrado

### Microcontroladores Testados
- **ESP32**: WiFi e Ethernet
- **Arduino**: Com módulos Ethernet W5100/W5500

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
