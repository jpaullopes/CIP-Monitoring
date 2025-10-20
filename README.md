# SensorFlow API

API backend para coleta de dados de processos CIP (Clean-in-Place). Recebe dados dos sensores via REST e disponibiliza.

## O que faz

Esta API coleta dados de **temperatura**, **concentração** e **fluxo** de processos CIP e:

- Detecta automaticamente quando um processo CIP começa e termina
- Mantém o último dado recebido em memória para consulta rápida
- Indica se o processo está ativo ou não (campo `active`)
- Persiste o estado em arquivo para não perder dados se o sistema cair
- **Autenticação JWT**: Protege endpoints com tokens JWT
- **Rate Limiting**: Limite de 20 requisições/minuto por dispositivo
- **Validação de Payload**: 3 níveis de proteção contra buffer overflow
- **Logging Estruturado**: Logs JSON com rastreamento de eventos

## Como usar

1. Sensores enviam dados via POST para `/api/sensor_data`
2. Consulta dados via GET em `/api/sensor_data` 
3. Se `active: true` → processo CIP rodando
4. Se `active: false` → processo terminou

## Tecnologias

### Backend & Framework
- **Python**: 3.11+
- **FastAPI**: Framework moderno e rápido com documentação automática
- **Uvicorn**: Servidor ASGI de alta performance

### Containerização & Orquestração
- **Docker**: Containerização da aplicação


3. **Execute com Docker Compose**
```bash
docker-compose up -d
```

4. **Acesse os serviços**

| Serviço    | URL                                        | Credenciais      |
|------------|--------------------------------------------|------------------|
| **API**    | [http://localhost:8000](http://localhost:8000) | JWT Bearer Token |


## Segurança

### Autenticação JWT

Todos os endpoints de escrita (`POST`) requerem autenticação via JWT Bearer Token.

**1. Obter Token (POST `/api/token`)**

```bash
curl -X POST "http://localhost:8000/api/token" \
  -H "Content-Type: application/json" \
  -d '{"device_id": "sensor_001"}'
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

**2. Usar Token em Requisições**

```bash
curl -X POST "http://localhost:8000/api/sensor_data" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"temperature": 75.5, "concentration": 0.8, "flow": 1.2}'
```

### Rate Limiting

- **Limite**: 20 requisições por minuto por dispositivo
- **Resposta ao exceder**: HTTP 429 com header `Retry-After`
- **Rastreamento**: Por device_id extraído do token JWT

### Proteção contra Buffer Overflow

3 níveis de validação:
1. **FastAPI**: Máximo 10 MB por requisição
2. **Middleware**: Validação customizada de tamanho
3. **Schema Pydantic**: Validação por campo (máx 1 KB)

### Logging Estruturado

- **Formato**: JSON estruturado com timestamp
- **Eventos**: Autenticação, rate limit, erros de validação
- **Proteção**: Sensores nunca são logados em produção
- **Armazenamento**: Rotação automática de logs (100 MB)


## API Endpoints


### Recepção de Dados dos Sensores

**POST** `/api/sensor_data`

Envia dados dos sensores CIP para o sistema. Requer autenticação JWT. O sistema gerencia automaticamente o CIP ID e detecta quando processos terminam.

**Requer:** `Authorization: Bearer <token>`

```bash
curl -X POST "http://localhost:8000/api/sensor_data" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 75.5,
    "concentration": 0.8,
    "flow": 1.2
  }'
```

**Respostas:**
- `201 Created`: Dados processados com sucesso
- `401 Unauthorized`: Token ausente ou inválido
- `429 Too Many Requests`: Limite de requisições excedido
- `413 Payload Too Large`: Tamanho da requisição excede 10 MB

### Consulta de Dados Mais Recentes

**GET** `/api/sensor_data`

Retorna os dados mais recentes com status do processo CIP. O campo `active` indica se o processo está em andamento.

```bash
curl -X GET "http://localhost:8000/api/sensor_data"
```

**Resposta:**
```json
{
  "temperature": 75.5,
  "concentration": 0.8,
  "flow": 1.2,
  "cip_id": 3,
  "timestamp": "2025-10-09T15:30:00-03:00",
  "active": true
}
```

## Funcionalidades Avançadas

### Sistema Antifail

O sistema mantém persistência do estado em arquivo JSON para recuperação após falhas:

- **Arquivo de estado**: `data/cip_state.json`
- **Recuperação automática**: Restaura CIP ID e status na inicialização

### Detecção Automática de Processos

- **Início**: Primeiro dado recebido inicia novo processo CIP
- **Fim**: Timeout sem receber dados marca processo como finalizado
- **Incremento automático**: CIP ID incrementa automaticamente a cada novo processo

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
