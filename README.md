# SensorFlow Server - InfluxDB Edition 🚀

[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-blue)](https://fastapi.tiangolo.com/)
[![InfluxDB](https://img.shields.io/badge/InfluxDB-v3.0+-orange)](https://influxdata.com/)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen)](https://github.com/jpaullopes/sensorflow-server-ethernet)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**SensorFlow Server - InfluxDB Edition** é uma solução backend moderna e escalável desenvolvida em Python/FastAPI para gerenciamento de dados de database em tempo real. Oferece persistência em **InfluxDB v3 com consultas SQL nativas**, visualização via Grafana, e comunicação bidirecional via WebSockets.

**Principais Diferenciais:**
- 🏗️ **Arquitetura Clean**: Organização modular seguindo princípios de Clean Architecture
- 🗄️ **InfluxDB v3**: Banco de dados de séries temporais com suporte SQL nativo
- 🔄 **Real-time**: WebSockets para streaming de dados em tempo real
- 🛡️ **Segurança**: Autenticação por API Key com controle granular

**Compatibilidade:** Este servidor funciona tanto com dispositivos conectados via **WiFi** quanto com **módulos Ethernet** (como W5500 ou W5100) sem necessidade de alterações no código.

---

## 🌟 Funcionalidades

### ✨ Core Features
- **API REST Segura**: Endpoints protegidos por API Key para recepção de dados de database
- **WebSocket em Tempo Real**: Distribuição instantânea de dados para clientes conectados
- **InfluxDB v3**: Armazenamento de séries temporais com consultas SQL nativas
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
- **Grafana**: Dashboards e visualização de dados
- **Health Endpoints**: Monitoramento da saúde da aplicação

### DevOps & Deployment
- **Docker**: Containerização da aplicação
- **Docker Compose**: Orquestração multi-container
- **Dockerfile**: Build automatizado da imagem

### Logging & Configuração
- **Pydantic Settings**: Gestão de configurações via env vars
- **Logging**: Sistema de logs estruturado 

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

Crie um arquivo `.env` na raiz, seguindo o exemplo do [`.env.example`](./.env.example).

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

```

## 🛣️ API Endpoints

### 📡 Recepção de Dados de database

**POST** `/api/v1/temperature_reading`

Endpoint principal para envio de dados de database, protegido por API Key.

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

**Exemplo CURL:**
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

Uma das principais vantagens desta versão é o suporte nativo a SQL no InfluxDB v3.

Execute consultas SQL diretamente no container InfluxDB:

```bash
# Listar 10 registros mais recentes
docker-compose exec influxdb3-core influxdb3 query \
  --token "$INFLUX_TOKEN" \
  --database "database" \
  "SELECT * FROM sensor_readings ORDER BY time DESC LIMIT 10"

```

## 📊 Integração Grafana

O SensorFlow Server implementa provisionamento automático do Grafana com InfluxDB v3 como fonte de dados, permitindo visualização imediata dos dados.

### 🔧 Provisionamento Automático

O sistema configura automaticamente:

- ✅ **Fonte de dados InfluxDB v3** pré-configurada
- ✅ **Conexão segura** com token e database via variáveis de ambiente
- ✅ **SQL Query Support** para consultas diretas nas tabelas
- ✅ **Dashboards pré-configurados** para monitoramento de database

### 🎨 Criação de Dashboards

1. **Acesse o Grafana**: [http://localhost:3000](http://localhost:3000)
2. **Login**: admin / admin123 (conforme configurado no .env)
3. **Novo Dashboard**: "+" → "Dashboard" → "Add new panel"
4. **Fonte de dados**: "InfluxDB v3 database" (pré-configurada)

```
## 🛡️ Segurança

O SensorFlow Server implementa múltiplas camadas de segurança:

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

-- database inativos (sem dados há mais de 1 hora)
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
    """Service para processamento de dados de database."""
    
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

## 🌐 Serviços

| Serviço       | Porta | Descrição                        | URL Local                        | Status |
|---------------|-------|----------------------------------|----------------------------------|---------|
| **🚀 API**    | 8000  | Backend FastAPI com Clean Arch   | http://localhost:8000           | ✅ Ativo |
| **📊 Docs**   | 8000  | Documentação Swagger/ReDoc       | http://localhost:8000/docs      | ✅ Ativo |
| **🗄️ InfluxDB** | 8181 | Banco de séries temporais v3    | http://localhost:8181           | ✅ Ativo |
| **📈 Grafana** | 3000 | Dashboards e visualização       | http://localhost:3000           | ✅ Ativo |
| **🌐 WebSocket** | 8000 | Real-time data streaming       | ws://localhost:8000/ws/sensor_updates | ✅ Ativo |

### 🔗 URLs Importantes

- **📖 API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs) - Interface Swagger
- **🔍 ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc) - Documentação alternativa  
- **🏥 Health**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health) - Status da aplicação
- **📊 Grafana**: [http://localhost:3000](http://localhost:3000) - admin/admin123

### ⚡ Status da Stack

```bash
# Verificar status de todos os serviços
docker-compose ps

# Saúde da aplicação
curl http://localhost:8000/api/v1/ping

# Verificar InfluxDB
docker-compose exec influxdb3-core influxdb3 query \
  --token "$INFLUX_TOKEN" \
  --database "database" \
  "SELECT COUNT(*) FROM sensor_readings"
```

---

## 📄 Licença

Este projeto está licenciado sob os termos da **licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

### 🚀 **SensorFlow Server - InfluxDB Edition**
**Desenvolvido com ❤️ em Python | FastAPI | InfluxDB v3**

*Uma solução moderna e escalável para IoT e monitoramento de database em tempo real.*


