# SensorFlow Server - InfluxDB Edition 🚀

[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-blue)](https://fastapi.tiangolo.com/)
[![InfluxDB](https://img.shields.io/badge/InfluxDB-v3.0+-orange)](https://influxdata.com/)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen)](https://github.com/jpaullopes/sensorflow-server-ethernet)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**SensorFlow Server - InfluxDB Edition** é uma solução backend moderna e escalável desenvolvida em Python/FastAPI para gerenciamento de dados de sensores em tempo real. Oferece persistência em **InfluxDB v3 com consultas SQL nativas**, visualização via Grafana, e comunicação bidirecional via WebSockets.

**Principais Diferenciais:**
- 🏗️ **Arquitetura Clean**: Organização modular seguindo princípios de Clean Architecture
- 🗄️ **InfluxDB v3**: Banco de dados de séries temporais com suporte SQL nativo
- 📊 **Consultas SQL**: Queries diretas no InfluxDB v3 via API REST
- 🔄 **Real-time**: WebSockets para streaming de dados em tempo real
- 🛡️ **Segurança**: Autenticação por API Key com controle granular

**Compatibilidade:** Este servidor funciona tanto com dispositivos conectados via **WiFi** quanto com **módulos Ethernet** (como W5500 ou W5100) sem necessidade de alterações no código.

---

## Índice

- [Funcionalidades](#funcionalidades)
- [Arquitetura](#-arquitetura)  
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [API Endpoints](#-api-endpoints)
- [Consultas SQL](#-consultas-sql-influxdb-v3)
- [Integração Grafana](#-integração-grafana)
- [Segurança](#-segurança)
- [Monitoramento](#-monitoramento)
- [Desenvolvimento](#-desenvolvimento)
- [Licença](#-licença)

## 🌟 Funcionalidades

### ✨ Core Features
- **API REST Segura**: Endpoints protegidos por API Key para recepção de dados de sensores
- **WebSocket em Tempo Real**: Distribuição instantânea de dados para clientes conectados
- **InfluxDB v3**: Armazenamento de séries temporais com **consultas SQL nativas**
- **Health Monitoring**: Endpoints de saúde para monitoramento da aplicação
- **Visualização com Grafana**: Dashboards personalizáveis para análise de dados

### 🏗️ Arquitetura Moderna
- **Clean Architecture**: Separação clara entre domínio, aplicação e infraestrutura
- **Injeção de Dependências**: Desacoplamento entre componentes
- **Configuração Externa**: Variáveis de ambiente para todas as configurações
- **Logs Estruturados**: Sistema avançado com níveis e formatação colorida

### 🔒 Segurança & Performance  
- **Autenticação Dupla**: API Keys independentes para HTTP e WebSocket
- **Limitação de Conexões**: Controle granular de conexões por API Key
- **Validação de Dados**: Schemas Pydantic para validação automática
- **SQL Injection Protection**: Consultas seguras via cliente oficial InfluxDB

### 🚀 DevOps & Deployment
- **Docker Compose**: Stack completa com orquestração de serviços
- **Healthchecks**: Verificação automática de saúde dos containers
- **Compatibilidade Ethernet**: Suporte nativo para módulos W5500 e W5100
- **CLI Tools**: Comandos diretos para interação com InfluxDB v3

## 🏗️ Arquitetura

O projeto segue **Clean Architecture** com separação clara de responsabilidades em camadas:

```plaintext
sensorflow-server-ethernet/
├── app/                           # 🚀 Camada de Aplicação
│   ├── main.py                   # Entry point FastAPI
│   ├── lifecycle.py              # Hooks de startup/shutdown
│   └── dependencies.py           # Injeção de dependências
├── src/                          # 📦 Código fonte modular
│   ├── api/v1/                   # 🛣️ Camada de Interface (Routers)
│   │   ├── routers/
│   │   │   ├── temperature.py    # Endpoints de sensores
│   │   │   ├── websocket.py      # WebSocket real-time
│   │   │   ├── health.py         # Health monitoring
│   │   │   └── query.py          # Consultas SQL InfluxDB
│   │   └── schemas/
│   │       └── temperature.py    # Modelos Pydantic
│   ├── core/                     # 💎 Camada de Domínio
│   │   ├── models/               # Entidades de negócio
│   │   └── services/             # Lógica de domínio
│   └── infrastructure/           # 🔧 Camada de Infraestrutura
│       ├── config/
│       │   └── settings.py       # Configurações da aplicação
│       ├── influx/
│       │   └── client.py         # Cliente InfluxDB v3
│       ├── logging/
│       │   └── config.py         # Sistema de logs
│       ├── security/
│       │   └── api_key.py        # Autenticação API Key
│       └── websocket/
│           └── manager.py        # Gerenciamento WebSocket
├── docker-compose.yml            # 🐳 Orquestração dos serviços
├── Dockerfile                    # 📦 Definição da imagem
├── requirements.txt              # 📋 Dependências Python
└── grafana/                      # 📊 Configuração Grafana
    └── provisioning/
        ├── datasources/          # InfluxDB datasource
        └── dashboards/           # Dashboards pré-configurados
```

### 🎯 Princípios Arquiteturais

- **Separation of Concerns**: Cada camada tem responsabilidades bem definidas
- **Dependency Inversion**: Abstrações não dependem de implementações
- **Single Responsibility**: Cada módulo tem uma única razão para mudar
- **Interface Segregation**: Interfaces específicas para cada cliente

## 🛠️ Tecnologias

### Backend & Framework
- **Python**: 3.11+
- **FastAPI**: Framework moderno e rápido com documentação automática
- **Uvicorn**: Servidor ASGI de alta performance
- **Pydantic**: Validação de dados e serialização

### Banco de Dados & Séries Temporais
- **InfluxDB v3**: Banco de dados de séries temporais com SQL nativo
- **influxdb_client_3**: Cliente Python oficial para InfluxDB v3

### Comunicação & Real-time
- **WebSockets**: Comunicação bidirecional em tempo real
- **API REST**: Endpoints HTTP para ingestão de dados

### Visualização & Monitoramento
- **Grafana OSS**: Dashboards e visualização de dados
- **Health Endpoints**: Monitoramento da saúde da aplicação

### DevOps & Deployment
- **Docker**: Containerização da aplicação
- **Docker Compose**: Orquestração multi-container
- **Dockerfile**: Build automatizado da imagem

### Logging & Configuração
- **Pydantic Settings**: Gestão de configurações via env vars
- **Logging**: Sistema de logs estruturado e colorido

## 🚀 Instalação

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

### ⚡ Configuração Rápida

1. **Clone o repositório**

```bash
git clone https://github.com/jpaullopes/sensorflow-server-ethernet.git
cd sensorflow-server-ethernet
```

2. **Configure o ambiente**

Crie um arquivo `.env` na raiz:

```dotenv
# 🔐 API Keys de Segurança
API_KEY=sua_chave_http_secreta_aqui
API_KEY_WS=sua_chave_websocket_secreta_aqui

# 🗄️ InfluxDB v3 Configuration
INFLUX_HOST=http://influxdb3-core:8181
INFLUX_TOKEN=apiv3_Q7UBMofejrm2UKcSBxcgZWsrq0F9yBplA1rOJcPJRYY8xaGV0H4yYLCQ3djH9f4tqPpVQUQGT6UmH2TuHJAV9Q==
INFLUX_DATABASE=sensores

# 🔗 Conexões & Limites  
MAX_WS_CONNECTIONS_PER_KEY=10

# 📊 Grafana
GF_SECURITY_ADMIN_PASSWORD=admin123
```

3. **Inicie a stack completa**

```bash
# Iniciar todos os serviços
docker-compose up -d

# Verificar status dos containers
docker-compose ps

# Acompanhar logs em tempo real
docker-compose logs -f api
```

4. **Acesse os serviços**

| Serviço    | URL                                        | Credenciais      |
|------------|--------------------------------------------|------------------|
| **API**    | [http://localhost:8000](http://localhost:8000) | API Key via header |
| **Docs**   | [http://localhost:8000/docs](http://localhost:8000/docs) | Interface Swagger |
| **InfluxDB**| [http://localhost:8181](http://localhost:8181) | Token via env    |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | admin/admin123  |

### 🔧 Comandos Úteis

```bash
# Rebuild apenas a API (após mudanças no código)
docker-compose up --build -d api

# Verificar logs específicos
docker-compose logs api        # Logs da API
docker-compose logs influxdb3-core  # Logs do InfluxDB
docker-compose logs grafana    # Logs do Grafana

# Parar todos os serviços
docker-compose down

# Limpar volumes (cuidado: apaga dados!)
docker-compose down -v
```

## 🛣️ API Endpoints

### 📡 Recepção de Dados de Sensores

**POST** `/api/v1/temperature_reading`

Endpoint principal para envio de dados de sensores, protegido por API Key.

**Headers necessários:**
- `X-API-Key`: Chave de autenticação para API
- `Content-Type`: application/json

**Payload:**
```json
{
  "temperature": 25.5,      // Temperatura em Celsius
  "humidity": 60.2,         // Umidade relativa (%)
  "pressure": 1012.5,       // Pressão atmosférica (hPa)  
  "sensor_id": "sensor_001" // ID único do sensor
}
```

**Resposta (201 Created):**
```json
{
  "id": 123,
  "temperature": 25.5,
  "humidity": 60.2,
  "pressure": 1012.5,
  "date_recorded": "2025-08-16",
  "time_recorded": "14:30:45",
  "sensor_id": "sensor_001",
  "client_ip": "192.168.1.100"
}
```

**Exemplo cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/temperature_reading" \
  -H "X-API-Key: sua_chave_http_secreta" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 25.5,
    "humidity": 60.2, 
    "pressure": 1012.5,
    "sensor_id": "sensor_001"
  }'
```

### 🏥 Health Monitoring

**GET** `/api/v1/health`

Endpoint completo de saúde da aplicação com informações detalhadas.

**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-16T15:30:45.123Z",
  "version": "2.1.0",
  "services": {
    "influxdb": "connected",
    "websocket_manager": "active"
  },
  "uptime_seconds": 3600
}
```

**GET** `/api/v1/ping`

Endpoint simples para verificação rápida (health check).

**Resposta:**
```json
{
  "status": "ok",
  "message": "SensorFlow API is running"
}
```

### 🔍 Consulta de Dados

**GET** `/api/v1/sensor/{sensor_id}/latest`

Busca o último registro de um sensor específico.

**Exemplo:**
```bash
curl -H "X-API-Key: sua_chave" \
  "http://localhost:8000/api/v1/sensor/sensor_001/latest"
```

### 🌐 WebSocket para Tempo Real

**WebSocket** `/ws/sensor_updates?api-key=sua_chave_websocket`

Conexão WebSocket para receber dados em tempo real conforme chegam na API.

**Parâmetros de Query:**
- `api-key`: Chave de autenticação para WebSocket (obrigatório)

**Exemplo JavaScript:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/sensor_updates?api-key=sua_chave_websocket');

ws.onopen = function() {
    console.log('🔌 Conectado ao WebSocket');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('📡 Novos dados:', data);
    // Atualizar dashboard em tempo real
};

ws.onclose = function() {
    console.log('🔌 Desconectado do WebSocket');
};
```

**Dados recebidos em tempo real:**
```json
{
  "temperature": 25.5,
  "humidity": 60.2, 
  "pressure": 1012.5,
  "sensor_id": "sensor_001",
  "timestamp": "2025-08-16T15:30:45.123Z"
}
```

##  API Endpoints

### Envio de Dados de Sensores

**POST** `/api/temperature_reading`

- **Descrição**: Recebe dados de sensores (temperatura, umidade e pressão)
- **Autenticação**: Header `X-API-Key` obrigatório
- **Content-Type**: `application/json`

**Exemplo de Requisição:**
```bash
curl -X POST "http://localhost:8000/api/temperature_reading" \
  -H "X-API-Key: sua_chave_http_secreta" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 25.5,
    "humidity": 60.2,
    "pressure": 1012.5,
    "sensor_id": "sensor_001"
  }'
```

**Resposta (201 Created):**
```json
{
  "id": 123,
  "temperature": 25.5,
  "humidity": 60.2,
  "pressure": 1012.5,
  "date_recorded": "2025-07-12",
  "time_recorded": "14:30:45",
  "sensor_id": "sensor_001",
  "client_ip": "192.168.1.100"
}
```

### WebSocket para Tempo Real

**WebSocket** `/ws/sensor_updates?api-key=sua_chave_websocket_secreta`

- **Descrição**: Recebe dados em tempo real conforme chegam na API
- **Autenticação**: Query parameter `api-key` obrigatório

**Exemplo JavaScript:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/sensor_updates?api-key=sua_chave_websocket_secreta');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Novos dados do sensor:', data);
    // Atualizar dashboard em tempo real
};
```

## Integração Grafana

O SensorFlow Server implementa provisionamento automático do Grafana, permitindo visualização imediata dos dados sem configuração manual.

### Provisionamento Automático

O sistema utiliza um mecanismo de provisionamento que configura automaticamente:

- Fonte de dados PostgreSQL
- Conexão segura com variáveis de ambiente
- Acesso direto à tabela de dados dos sensores

### Criação de Dashboards

1. Acesse o Grafana em [http://localhost:3000](http://localhost:3000)
2. Faça login com as credenciais (admin/sua_senha)
3. Crie um novo dashboard: "+" → "Dashboard" → "Add new panel"
4. A fonte de dados "PostgreSQL Sensores" estará disponível para consultas

**Exemplo de Query SQL:**
```sql
SELECT 
  date_recorded + time_recorded as time, 
  temperature, 
  humidity, 
  pressure
FROM data 
WHERE 
  $__timeFilter(date_recorded + time_recorded) AND
  sensor_id = 'sensor_001'
```

## Segurança

O SensorFlow Server implementa múltiplas camadas de segurança:

- **API Keys Independentes**: Separação de chaves entre HTTP e WebSocket
- **Limitação de Conexões**: Controle configurável de conexões por API Key
- **Validação de Dados**: Validação automática via Pydantic
- **Sanitização de Inputs**: Proteção contra injeção SQL
- **Logs Detalhados**: Rastreamento de atividades para auditoria

A configuração de segurança é gerenciada através do arquivo `.env`, permitindo customização sem alteração de código.

## Monitoramento

O sistema fornece recursos avançados de monitoramento:

### Logs de Serviços

```bash
# Monitorar todos os serviços
docker-compose logs -f

# Filtrar por serviço específico
docker-compose logs -f api
docker-compose logs -f db
docker-compose logs -f grafana
```

### Métricas Disponíveis

- Latência de processamento de requests
- Taxa de ingestão de dados
- Conexões WebSocket ativas
- Estatísticas de uso do banco de dados

## Desenvolvimento

### Princípios de Design

O SensorFlow Server foi construído seguindo princípios de engenharia de software modernos:

- **Separação de Responsabilidades**: Cada módulo tem um propósito específico
- **Injeção de Dependências**: Redução de acoplamento entre componentes
- **Abstração de Dados**: Interfaces bem definidas entre camadas
- **Configuração Externa**: Parâmetros definidos via variáveis de ambiente
- **Testabilidade**: Estrutura projetada para facilitar testes unitários e de integração

### Extensão da Aplicação

O projeto foi projetado para ser extensível. Você pode:

- Adicionar novos tipos de sensores
- Implementar novas estratégias de autenticação
- Criar endpoints personalizados
- Expandir a lógica de processamento de dados

### Contribuição

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Implemente suas mudanças com testes apropriados
4. Documente alterações no README, se necessário
5. Envie um Pull Request com descrição detalhada das mudanças

## Serviços

| Serviço    | Porta | Descrição                  | URL Local                   |
|------------|-------|----------------------------|----------------------------|
| **API**    | 8000  | Backend FastAPI            | http://localhost:8000      |
| **DB**     | 5432  | Banco de dados PostgreSQL  | postgresql://localhost:5432 |
| **Grafana**| 3000  | Visualização de dados      | http://localhost:3000      |

## Licença

Este projeto está licenciado sob os termos da licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.


