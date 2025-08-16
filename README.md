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

## 🗄️ Consultas SQL - InfluxDB v3

Uma das principais vantagens desta versão é o **suporte nativo a SQL** no InfluxDB v3.

### 🔧 Via API REST

**POST** `/api/v1/query`

Execute consultas SQL diretamente no InfluxDB v3 via API.

**Headers:**
- `X-API-Key`: Chave de autenticação
- `Content-Type`: application/json

**Payload:**
```json
{
  "query": "SELECT * FROM sensor_readings ORDER BY time DESC LIMIT 10"
}
```

**Exemplo cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "X-API-Key: sua_chave_http_secreta" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM sensor_readings ORDER BY time DESC LIMIT 10"}'
```

### 💻 Via CLI (Docker)

Execute consultas SQL diretamente no container InfluxDB:

```bash
# Listar 10 registros mais recentes
docker-compose exec influxdb3-core influxdb3 query \
  --token "$INFLUX_TOKEN" \
  --database "sensores" \
  "SELECT * FROM sensor_readings ORDER BY time DESC LIMIT 10"

# Contar total de registros
docker-compose exec influxdb3-core influxdb3 query \
  --token "$INFLUX_TOKEN" \
  --database "sensores" \
  "SELECT COUNT(*) FROM sensor_readings"

# Dados de um sensor específico nas últimas 24h
docker-compose exec influxdb3-core influxdb3 query \
  --token "$INFLUX_TOKEN" \
  --database "sensores" \
  "SELECT * FROM sensor_readings 
   WHERE sensor_id = 'sensor_001' 
   AND time > now() - interval '24 hours'"

# Média de temperatura por sensor
docker-compose exec influxdb3-core influxdb3 query \
  --token "$INFLUX_TOKEN" \
  --database "sensores" \
  "SELECT sensor_id, AVG(temperature) as avg_temp 
   FROM sensor_readings 
   GROUP BY sensor_id"
```

### 📊 Estrutura dos Dados

Os dados são armazenados na tabela `sensor_readings` com a seguinte estrutura:

| Coluna        | Tipo      | Descrição                    |
|---------------|-----------|------------------------------|
| `time`        | Timestamp | Momento da leitura (automático) |
| `sensor_id`   | String    | Identificador único do sensor |
| `client_ip`   | String    | IP do cliente que enviou     |
| `temperature` | Float     | Temperatura em Celsius       |
| `humidity`    | Float     | Umidade relativa (%)         |
| `pressure`    | Float     | Pressão atmosférica (hPa)    |

### 🔍 Consultas Úteis

```sql
-- 📈 Tendência de temperatura nas últimas 2 horas
SELECT 
  time,
  sensor_id,
  temperature,
  LAG(temperature) OVER (PARTITION BY sensor_id ORDER BY time) as prev_temp
FROM sensor_readings 
WHERE time > now() - interval '2 hours'
ORDER BY time DESC;

-- 🌡️ Sensores com temperatura crítica
SELECT DISTINCT sensor_id, MAX(temperature) as max_temp
FROM sensor_readings 
WHERE temperature > 30
GROUP BY sensor_id;

-- 📊 Estatísticas por sensor (última hora)
SELECT 
  sensor_id,
  COUNT(*) as readings_count,
  AVG(temperature) as avg_temp,
  MIN(temperature) as min_temp,
  MAX(temperature) as max_temp,
  AVG(humidity) as avg_humidity
FROM sensor_readings 
WHERE time > now() - interval '1 hour'
GROUP BY sensor_id;
```

## 📊 Integração Grafana

O SensorFlow Server implementa provisionamento automático do Grafana com **InfluxDB v3** como fonte de dados, permitindo visualização imediata dos dados.

### 🔧 Provisionamento Automático

O sistema configura automaticamente:

- ✅ **Fonte de dados InfluxDB v3** pré-configurada
- ✅ **Conexão segura** com token e database via variáveis de ambiente
- ✅ **SQL Query Support** para consultas diretas nas tabelas
- ✅ **Dashboards pré-configurados** para monitoramento de sensores

### 🎨 Criação de Dashboards

1. **Acesse o Grafana**: [http://localhost:3000](http://localhost:3000)
2. **Login**: admin / admin123 (conforme configurado no .env)
3. **Novo Dashboard**: "+" → "Dashboard" → "Add new panel"
4. **Fonte de dados**: "InfluxDB v3 Sensores" (pré-configurada)

### 🔍 Queries SQL para Dashboards

**Temperatura em Tempo Real:**
```sql
SELECT 
  time as "time",
  temperature,
  sensor_id
FROM sensor_readings 
WHERE $__timeFilter(time)
  AND sensor_id = '$sensor_id'
ORDER BY time DESC
```

**Múltiplos Sensores (Series):**
```sql
SELECT 
  time as "time",
  temperature,
  sensor_id as "metric"  
FROM sensor_readings 
WHERE $__timeFilter(time)
GROUP BY sensor_id
ORDER BY time DESC
```

**Estatísticas por Período:**
```sql
SELECT 
  time_bucket('5 minutes', time) as "time",
  sensor_id,
  AVG(temperature) as avg_temperature,
  AVG(humidity) as avg_humidity,
  AVG(pressure) as avg_pressure
FROM sensor_readings 
WHERE $__timeFilter(time)
GROUP BY time_bucket('5 minutes', time), sensor_id
ORDER BY time
```

**Status de Conexão dos Sensores:**
```sql
SELECT 
  sensor_id,
  MAX(time) as last_seen,
  COUNT(*) as total_readings
FROM sensor_readings 
WHERE $__timeFilter(time)
GROUP BY sensor_id
```

### 📈 Tipos de Visualização Recomendados

| Métrica | Tipo de Painel | Query |
|---------|----------------|-------|
| **Temperatura** | Time Series | `SELECT time, temperature, sensor_id FROM sensor_readings` |
| **Umidade** | Gauge | `SELECT AVG(humidity) FROM sensor_readings WHERE time > now() - interval '1 hour'` |
| **Pressão** | Stat | `SELECT pressure FROM sensor_readings ORDER BY time DESC LIMIT 1` |
| **Status Sensores** | Table | `SELECT sensor_id, MAX(time) as last_update FROM sensor_readings GROUP BY sensor_id` |

### 🚨 Alertas e Notificações

Configure alertas baseados em thresholds:

```sql
-- Alerta de temperatura alta
SELECT 
  sensor_id,
  temperature,
  time
FROM sensor_readings 
WHERE temperature > 35
  AND time > now() - interval '5 minutes'
```

### 🔧 Variáveis de Dashboard

Crie variáveis para dashboards dinâmicos:

**Variable `sensor_id`:**
```sql
SELECT DISTINCT sensor_id FROM sensor_readings
```

**Variable `time_range`:**
- Custom: `1h,6h,24h,7d`

Isso permite dashboards interativos onde o usuário pode filtrar por sensor e período de tempo.

## 🛡️ Segurança

O SensorFlow Server implementa múltiplas camadas de segurança empresariais:

### 🔐 Autenticação por API Key
- **Chaves Independentes**: Separação entre HTTP (`API_KEY`) e WebSocket (`API_KEY_WS`)
- **Headers Seguros**: Autenticação via `X-API-Key` header
- **Validação Automática**: Middleware de autenticação em todos os endpoints protegidos

### 🚧 Controle de Acesso
- **Limitação de Conexões**: Máximo configurável de conexões WebSocket por API Key
- **Validação de Origem**: Tracking de IP do cliente para auditoria
- **Sanitização de Inputs**: Validação automática via schemas Pydantic

### 🔒 Proteções Implementadas
- **SQL Injection**: Consultas preparadas via cliente oficial InfluxDB
- **CORS**: Configuração de Cross-Origin Resource Sharing
- **Rate Limiting**: Prevenção de abuso de endpoints
- **Logs de Auditoria**: Rastreamento detalhado de todas as operações

### 📋 Configuração de Segurança

```dotenv
# Chaves de 32+ caracteres recomendadas
API_KEY=sua_chave_http_muito_secreta_e_longa_aqui
API_KEY_WS=sua_chave_websocket_muito_secreta_e_longa_aqui

# Controle de conexões
MAX_WS_CONNECTIONS_PER_KEY=10

# InfluxDB Token seguro (gerado automaticamente)
INFLUX_TOKEN=apiv3_Q7UBMofejrm2UKcSBxcgZWsrq0F9yBplA1rOJcPJRYY...
```

## 📈 Monitoramento

### 🏥 Health Endpoints

- **`GET /api/v1/health`**: Status completo da aplicação
- **`GET /api/v1/ping`**: Verificação rápida de saúde

### 📊 Logs de Aplicação

```bash
# Logs em tempo real
docker-compose logs -f api

# Logs específicos por serviço
docker-compose logs influxdb3-core  # InfluxDB
docker-compose logs grafana         # Grafana

# Filtrar por nível de log
docker-compose logs api | grep ERROR
docker-compose logs api | grep INFO
```

### 📈 Métricas Disponíveis

- **Latência de Requests**: Tempo de processamento de cada endpoint
- **Taxa de Ingestão**: Dados recebidos por minuto/hora
- **Conexões WebSocket**: Número de conexões ativas
- **Health Status**: Estado de saúde do InfluxDB e demais serviços
- **Uso de Recursos**: Memory usage, CPU, Network I/O

### 🚨 Alertas e Monitoramento

**Via Logs:**
```bash
# Monitorar erros críticos
docker-compose logs api | grep "ERROR\|CRITICAL"

# Monitorar conexões WebSocket
docker-compose logs api | grep "WebSocket"

# Monitorar ingestão de dados
docker-compose logs api | grep "temperature_reading"
```

**Via InfluxDB (Queries de Monitoramento):**
```sql
-- Taxa de ingestão por hora
SELECT 
  date_trunc('hour', time) as hour,
  COUNT(*) as readings_per_hour
FROM sensor_readings 
WHERE time > now() - interval '24 hours'
GROUP BY hour
ORDER BY hour;

-- Sensores inativos (sem dados há mais de 1 hora)
SELECT DISTINCT sensor_id, MAX(time) as last_reading
FROM sensor_readings 
GROUP BY sensor_id
HAVING MAX(time) < now() - interval '1 hour';
```

## 🧑‍💻 Desenvolvimento

### 🎯 Princípios de Design

O SensorFlow Server segue **Clean Architecture** e princípios SOLID:

- **🔄 Separation of Concerns**: Cada camada tem responsabilidades bem definidas
- **📦 Dependency Inversion**: Abstrações não dependem de implementações
- **🎯 Single Responsibility**: Cada módulo tem uma única razão para mudar
- **🔧 Interface Segregation**: Interfaces específicas para cada necessidade
- **🔀 Open/Closed**: Aberto para extensão, fechado para modificação

### 🏗️ Estrutura do Código

```plaintext
src/
├── api/v1/                  # 🌐 Interface Layer (Controllers)
│   ├── routers/            # FastAPI routers
│   └── schemas/            # Request/Response models
├── core/                   # 💎 Domain Layer (Business Logic)
│   ├── models/            # Domain entities
│   └── services/          # Business rules
└── infrastructure/        # 🔧 Infrastructure Layer (External)
    ├── config/           # Configuration management
    ├── influx/           # Database client
    ├── logging/          # Logging system
    ├── security/         # Authentication
    └── websocket/        # WebSocket manager
```

### 🔧 Desenvolvimento Local

#### Configurar Ambiente de Desenvolvimento:

```bash
# 1. Clone e entre no diretório
git clone https://github.com/jpaullopes/sensorflow-server-ethernet.git
cd sensorflow-server-ethernet

# 2. Crie ambiente virtual Python
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure .env para desenvolvimento
cp .env.example .env      # Ajuste as variáveis
```

#### Executar em Modo Desenvolvimento:

```bash
# Apenas InfluxDB (desenvolvimento da API)
docker-compose up -d influxdb3-core

# API em desenvolvimento (hot reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Todos os serviços
docker-compose up -d
```

### 🧪 Testes

```bash
# Testes unitários
python -m pytest tests/

# Testes com coverage
python -m pytest tests/ --cov=src

# Testes de integração
python -m pytest tests/integration/

# Linting e formatação
flake8 src/
black src/
isort src/
```

### 📦 Extensibilidade

#### Adicionar Novo Tipo de Sensor:

1. **Schema** (src/api/v1/schemas/):
```python
# new_sensor.py
from pydantic import BaseModel

class NewSensorReading(BaseModel):
    sensor_id: str
    custom_value: float
    # ... outros campos
```

2. **Router** (src/api/v1/routers/):
```python
# new_sensor.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/new_sensor_reading")
async def receive_data(data: NewSensorReading):
    # ... lógica de processamento
```

3. **Registrar Router** (src/api/v1/routers/__init__.py):
```python
from .new_sensor import router as new_sensor_router

api_v1_router.include_router(new_sensor_router, tags=["new_sensor"])
```

#### Adicionar Nova Funcionalidade:

1. **Service** (src/core/services/):
```python
# analytics.py
class AnalyticsService:
    def calculate_trends(self, sensor_data):
        # Lógica de negócio
        pass
```

2. **Infrastructure** (src/infrastructure/):
```python
# external_api.py  
class ExternalAPIClient:
    def send_alert(self, data):
        # Integração externa
        pass
```

### 🤝 Contribuição

#### Fluxo de Contribuição:

1. **Fork** do repositório
2. **Branch** para sua feature: `git checkout -b feature/nova-funcionalidade`
3. **Implementar** com testes apropriados
4. **Documentar** alterações no README (se necessário)
5. **Pull Request** com descrição detalhada

#### Padrões de Código:

- **Docstrings**: Google Style para todas as funções
- **Type Hints**: Obrigatório para parâmetros e retornos
- **Error Handling**: Try/catch com logs apropriados
- **Testes**: Cobertura mínima de 80%

#### Exemplo de Implementação:

```python
from typing import Optional
from src.infrastructure.influx.client import InfluxClient

class SensorService:
    """Service para processamento de dados de sensores."""
    
    def __init__(self, influx_client: InfluxClient):
        """
        Args:
            influx_client: Cliente InfluxDB para persistência.
        """
        self.influx_client = influx_client
    
    async def process_reading(self, reading: dict) -> Optional[dict]:
        """
        Processa leitura de sensor e persiste no InfluxDB.
        
        Args:
            reading: Dados do sensor validados.
            
        Returns:
            Dados processados ou None em caso de erro.
            
        Raises:
            ProcessingError: Se falhar no processamento.
        """
        try:
            # Lógica de processamento
            result = await self.influx_client.write_data(reading)
            return result
        except Exception as e:
            logger.error(f"Erro ao processar leitura: {e}")
            raise ProcessingError(f"Falha no processamento: {e}")
```

### 🔍 Debug e Troubleshooting

```bash
# Logs detalhados da aplicação
docker-compose logs -f api

# Acesso ao container para debug
docker-compose exec api /bin/bash

# Verificar conectividade InfluxDB
docker-compose exec api python -c "
from src.infrastructure.influx.client import get_influx_client
client = get_influx_client()
print('InfluxDB conectado:', client is not None)
"

# Testar endpoints manualmente
curl -H "X-API-Key: sua_chave" http://localhost:8000/api/v1/health
```

## Serviços

| Serviço    | Porta | Descrição                  | URL Local                   |
|------------|-------|----------------------------|----------------------------|
| **API**    | 8000  | Backend FastAPI            | http://localhost:8000      |
| **DB**     | 5432  | Banco de dados PostgreSQL  | postgresql://localhost:5432 |
| **Grafana**| 3000  | Visualização de dados      | http://localhost:3000      |

## Licença

Este projeto está licenciado sob os termos da licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.


