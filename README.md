# SensorFlow Server

[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-blue)](https://fastapi.tiangolo.com/)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen)](https://github.com/jpaullopes/sensorflow-server)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**SensorFlow Server** é uma solução backend escalável e resiliente desenvolvida em Python/FastAPI para gerenciamento de dados de sensores em tempo real. Oferece persistência em PostgreSQL, visualização via Grafana, e comunicação bidirecional via WebSockets.

---

## � Índice

- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [API Endpoints](#-api-endpoints)
- [Integração Grafana](#-integração-grafana)
- [Segurança](#-segurança)
- [Monitoramento](#-monitoramento)
- [Desenvolvimento](#-desenvolvimento)
- [Licença](#-licença)

## 🚀 Funcionalidades

- **API REST Segura**: Endpoints protegidos por API Key para recepção de dados de sensores
- **WebSocket em Tempo Real**: Distribuição instantânea de dados para clientes conectados
- **Banco de Dados PostgreSQL**: Armazenamento persistente com schemas auto-gerenciados
- **Visualização com Grafana**: Dashboards personalizáveis para análise de dados
- **Autenticação Dupla**: API Keys independentes para HTTP e WebSocket
- **Limitação de Conexões**: Controle granular de conexões por API Key
- **Logs Estruturados**: Sistema avançado com níveis e formatação colorida
- **Arquitetura Modular**: Código organizado por responsabilidades
- **Docker Compose**: Stack completa com orquestração de serviços

## 🏗️ Arquitetura

O projeto segue um padrão de arquitetura modular, com separação clara de responsabilidades:

```plaintext
sensorflow-server/
├── main.py                   # Ponto de entrada da aplicação
├── src/                      # Código fonte modular
│   ├── config.py            # Configurações e variáveis de ambiente
│   ├── logger_config.py     # Sistema de logs coloridos
│   ├── models.py            # Modelos SQLAlchemy e Pydantic
│   ├── database.py          # Configuração e conexão do banco
│   ├── auth.py              # Autenticação e verificação de API Keys
│   ├── websocket_manager.py # Gerenciamento de conexões WebSocket
│   └── routes/              # Endpoints organizados por domínio
├── docker-compose.yml        # Orquestração dos serviços
├── Dockerfile                # Definição da imagem de contêiner
├── requirements.txt          # Dependências Python
├── grafana/                  # Configuração do Grafana
│   └── provisioning/         # Provisionamento automático
│       └── datasources/      # Fontes de dados pré-configuradas
└── README.md                 # Documentação do projeto
```

## �️ Tecnologias

- **Backend**: Python 3.9+, FastAPI
- **Banco de Dados**: PostgreSQL 13+
- **ORM**: SQLAlchemy 2.0+
- **Validação**: Pydantic v2
- **Comunicação**: WebSockets
- **Visualização**: Grafana OSS
- **Contêineres**: Docker, Docker Compose
- **Logging**: ColorLog

## ⚙️ Instalação

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

### Configuração Rápida

1. **Clone o repositório**

```bash
git clone https://github.com/jpaullopes/sensorflow-server.git
cd sensorflow-server
```

2. **Configure o ambiente**

Crie um arquivo `.env` na raiz:

```dotenv
# API Keys de segurança
API_KEY=sua_chave_http_secreta
API_KEY_WS=sua_chave_websocket_secreta

# PostgreSQL
POSTGRES_USER=sensoruser
POSTGRES_PASSWORD=sensorpass
POSTGRES_DB=sensordb
DATABASE_URL=postgresql://sensoruser:sensorpass@db:5432/sensordb

# Limites de conexão
MAX_WS_CONNECTIONS_PER_KEY=10

# Grafana
GF_SECURITY_ADMIN_PASSWORD=admin123
```

3. **Inicie a stack**

```bash
docker-compose up -d
```

4. **Acesse os serviços**

- **API**: [http://localhost:8000](http://localhost:8000)
- **Grafana**: [http://localhost:3000](http://localhost:3000) (admin/sua_senha)

## � API Endpoints

### Recepção de Dados de Sensores

**POST** `/api/temperature_reading`

Endpoint para envio de dados de sensores, protegido por API Key.

**Headers necessários:**
- `X-API-Key`: Chave de autenticação para API
- `Content-Type`: application/json

**Payload:**
```json
{
  "temperature": 25.5,    // Temperatura em Celsius
  "humidity": 60.2,       // Umidade relativa (%)
  "pressure": 1012.5,     // Pressão atmosférica (hPa)
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
  "date_recorded": "2023-07-12",
  "time_recorded": "14:30:45",
  "sensor_id": "sensor_001",
  "client_ip": "192.168.1.100"
}
```

### WebSocket para Tempo Real

**Endpoint:** `/ws/sensor_updates`

Conexão WebSocket para receber dados em tempo real.

**Parâmetros de Query:**
- `api-key`: Chave de autenticação para WebSocket

**Exemplo JavaScript:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/sensor_updates?api-key=sua_chave_websocket');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Dados recebidos:', data);
    // Processamento em tempo real
};
```

## 📡 API Endpoints

### 🌡️ Envio de Dados de Sensores

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

### 🔌 WebSocket para Tempo Real

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

## 📊 Integração Grafana

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

## 🔒 Segurança

O SensorFlow Server implementa múltiplas camadas de segurança:

- **API Keys Independentes**: Separação de chaves entre HTTP e WebSocket
- **Limitação de Conexões**: Controle configurável de conexões por API Key
- **Validação de Dados**: Validação automática via Pydantic
- **Sanitização de Inputs**: Proteção contra injeção SQL
- **Logs Detalhados**: Rastreamento de atividades para auditoria

A configuração de segurança é gerenciada através do arquivo `.env`, permitindo customização sem alteração de código.

## 📝 Monitoramento

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

## 🔍 Desenvolvimento

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

## 📊 Serviços

| Serviço    | Porta | Descrição                  | URL Local                   |
|------------|-------|----------------------------|----------------------------|
| **API**    | 8000  | Backend FastAPI            | http://localhost:8000      |
| **DB**     | 5432  | Banco de dados PostgreSQL  | postgresql://localhost:5432 |
| **Grafana**| 3000  | Visualização de dados      | http://localhost:3000      |

## 📄 Licença

Este projeto está licenciado sob os termos da licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.


