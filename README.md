# SensorFlow API

API backend para coleta de dados de processos CIP (Clean-in-Place). Recebe dados dos sensores via REST e disponibiliza.

## O que faz

Esta API coleta dados de **temperatura**, **concentração** e **fluxo** de processos CIP e:

- Detecta automaticamente quando um processo CIP começa e termina
- Mantém o último dado recebido em memória para consulta rápida
- Indica se o processo está ativo ou não (campo `active`)
- Persiste o estado em arquivo para não perder dados se o sistema cair

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
| **API**    | [http://localhost:8000](http://localhost:8000) | API Key via header |


## API Endpoints

### Recepção de Dados dos Sensores

**POST** `/api/sensor_data`

Envia dados dos sensores CIP para o sistema. O sistema gerencia automaticamente o CIP ID e detecta quando processos terminam.

```bash
curl -X POST "http://localhost:8000/api/sensor_data" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 75.5,
    "concentration": 0.8,
    "flow": 1.2
  }'
```

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
