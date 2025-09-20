# Documentação Técnica - SensorFlow API

## Visão Geral da Arquitetura

Este projeto implementa uma API REST para coleta de dados de sensores com transmissão em tempo real via WebSocket. A arquitetura segue o padrão Clean Architecture com separação clara entre camadas.

### Estrutura de Diretórios

```
src/
├── api/
│   ├── routers/
│   └── schemas/
└── infrastructure/
    ├── config/
    ├── security/
    ├── websocket/
    └── logging/
```

---

## Módulos da API

### [`src/api/schemas/temperature.py`](./src/api/schemas/temperature.py)

**Propósito**: Define modelos Pydantic para validação e serialização de dados de sensores.

#### Classes

**`SensorDataPayload(BaseModel)`**
- **Responsabilidade**: Validação de dados de entrada da placa.
- **Campos**:
  - `pressure: float`
  - `temperature: float`
  - `concentration: float`
  - `flow: float`
- **Código**:
  ```python
  class SensorDataPayload(BaseModel):
      pressure: float
      temperature: float
      concentration: float
      flow: float
  ```

**`SensorDataResponse(BaseModel)`**
- **Responsabilidade**: Formato de resposta padronizado.
- **Campos**:
  - `temperature: float`
  - `pressure: float`
  - `concentration: float`
  - `flow: float`
  - `timestamp: datetime`
  - `cip_id: int`
- **Código**:
  ```python
  class SensorDataResponse(BaseModel):
      pressure: float
      temperature: float
      concentration: float
      flow: float
      timestamp: datetime
      cip_id: int
  ```

---

### [`src/api/routers/temperature.py`](./src/api/routers/temperature.py)

**Propósito**: Implementa endpoints para coleta e consulta de dados de sensores com lógica de CIP automático.

#### Variáveis Globais

```python
latest_sensor_data: SensorDataResponse = None
current_cip_id: int = 1
last_data_timestamp: datetime = None
CIP_TIMEOUT_MINUTES = 10
```

#### Endpoints

**`POST /sensor_data`**
- **Autenticação**: Requer API Key (`verify_api_key`).
- **Payload**: `SensorDataPayload`.
- **Lógica CIP**:
  1. Calcula diferença de tempo desde o último envio.
  2. Se for maior que 10 minutos, incrementa `current_cip_id`.
  3. Atualiza `last_data_timestamp`.
- **Processamento**:
  1. Gera timestamp com timezone do Brasil.
  2. Cria `SensorDataResponse` com dados e CIP ID.
  3. Armazena em cache (`latest_sensor_data`).
  4. Broadcast via WebSocket para clientes conectados.
- **Retorno**: `SensorDataResponse` com dados processados.

**`GET /sensor_data`**
- **Autenticação**: Pública (sem API Key).
- **Lógica**:
  1. Retorna `latest_sensor_data` se disponível.
  2. Se o cache estiver vazio, retorna dados zerados com o CIP ID atual.
- **Uso**: Outras aplicações consultam os dados mais recentes.

#### Algoritmo de CIP Automático

```python
if last_data_timestamp is not None:
    time_diff = brasilia_now - last_data_timestamp
    if time_diff > timedelta(minutes=CIP_TIMEOUT_MINUTES):
        current_cip_id += 1
        logger.info(f"CIP ID incrementado para {current_cip_id}...")
last_data_timestamp = brasilia_now
```

---

### [`src/api/routers/health.py`](./src/api/routers/health.py)

**Propósito**: Endpoint simples para monitoramento de saúde da aplicação.

#### Endpoints

**`GET /health`**
- **Autenticação**: Pública.
- **Resposta**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2025-09-17T18:30:45.123456+00:00",
    "service": "SensorFlow API"
  }
  ```
- **Código**:
  ```python
  @router.get("/health", status_code=status.HTTP_200_OK)
  async def health_check():
      return {
          "status": "healthy",
          "timestamp": datetime.now(timezone.utc).isoformat(),
          "service": "SensorFlow API"
      }
  ```

---

### [`src/api/routers/websocket.py`](./src/api/routers/websocket.py)

**Propósito**: Endpoint WebSocket para transmissão de dados em tempo real.

#### Endpoints

**`WS /sensor_updates`**
- **Autenticação**: API Key via query parameter `?api-key=xxx`.
- **Fluxo de Conexão**:
  1. Valida a API key com `verify_ws_api_key`.
  2. Se inválida, fecha a conexão com código 1008.
  3. Se válida, aceita via `manager.connect()`.
- **Ciclo de Vida**:
  1. Aceita a conexão.
  2. Loop infinito aguardando mensagens (keep-alive).
  3. Em desconexão, faz o cleanup via `manager.disconnect()`.

---

### [`src/api/routers/__init__.py`](./src/api/routers/__init__.py)

**Propósito**: Agrega todos os routers em um router principal.

#### Configuração

```python
api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(temperature_router, tags=["sensor"])
api_v1_router.include_router(health_router, tags=["health"])
```
- **`prefix`**: Todos os endpoints ficam sob `/api/v1/`.
- **`tags`**: Organizam os endpoints na documentação Swagger.

---

## Fluxo de Dados Completo

### 1. Envio de Dados (Placa → API)

```
Placa/Sensor
    ↓ POST /api/v1/sensor_data + API Key
Temperature Router
    ↓ Validação + Lógica CIP
Cache em Memória (latest_sensor_data)
    ↓ Broadcast
WebSocket Manager
    ↓ JSON
Clientes WebSocket Conectados
```

### 2. Consulta de Dados (App → API)

```
Aplicação Cliente
    ↓ GET /api/v1/sensor_data (sem auth)
Temperature Router
    ↓ Leitura do cache
latest_sensor_data
    ↓ JSON Response
Aplicação Cliente
```

### 3. Tempo Real (WebSocket)

```
Cliente WebSocket
    ↓ Conexão + API Key WS
WebSocket Router
    ↓ Autenticação
Connection Manager
    ↓ Keep-alive
[Aguarda broadcast quando POST acontece]
```

---

## Módulos da Infraestrutura

### [`src/infrastructure/config/settings.py`](./src/infrastructure/config/settings.py)

**Propósito**: Gerenciamento centralizado de configurações usando Pydantic Settings.

#### Classes

**`Settings(BaseSettings)`**
- **Responsabilidade**: Carrega e valida configurações de ambiente.
- **Campos**:
  - `API_KEY`, `API_KEY_WS`, `MAX_WS_CONNECTIONS_PER_KEY`.

#### Funções

**`get_settings()`**
- **Decorador**: `@lru_cache` para cachear a instância.
- **Retorno**: Instância singleton de `Settings`.

---

### [`src/infrastructure/security/api_key.py`](./src/infrastructure/security/api_key.py)

**Propósito**: Implementa autenticação baseada em API Key para HTTP e WebSocket.

#### Funções

**`verify_api_key(x_api_key: str)`**
- **Tipo**: Dependency do FastAPI.
- **Validação**: Compara a chave do header com `settings.API_KEY`.
- **Exceção**: `HTTPException 401` se inválida.

**`verify_ws_api_key(api_key: str)`**
- **Tipo**: Função assíncrona para WebSocket.
- **Validação**: Compara a chave da query com `settings.API_KEY_WS`.
- **Retorno**: `True/False`.

---

### [`src/infrastructure/websocket/manager.py`](./src/infrastructure/websocket/manager.py)

**Propósito**: Gerencia conexões WebSocket ativas e broadcast de mensagens.

#### Classes

**`ConnectionManager`**
- **Padrão**: Singleton para gerenciamento global.
- **Atributos**:
  - `active_connections: List[WebSocket]`
  - `connections_per_key: Dict[str, int]`

#### Métodos

**`connect(websocket: WebSocket, api_key: str)`**
- **Fluxo**: Aceita a conexão, adiciona à lista de ativas e incrementa o contador por chave.

**`disconnect(websocket: WebSocket)`**
- **Fluxo**: Remove da lista de conexões ativas.

**`broadcast_json(data)`**
- **Fluxo**: Itera sobre as conexões ativas, envia dados JSON e remove conexões com erro.

---

### [`src/infrastructure/logging/config.py`](./src/infrastructure/logging/config.py)

**Propósito**: Configuração padronizada de logging com cores.

#### Funções

**`get_logger(name: str)`**
- **Configuração**: Define o formato, data e cores do log.
- **Retorno**: Logger configurado e pronto para uso.
- **Padrão**: Singleton por nome para evitar reconfiguração.