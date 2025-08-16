from fastapi import APIRouter, status, Depends, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List
from src.infrastructure.influx.client import query_sensor_data_sql, get_client
from src.infrastructure.security.api_key import verify_api_key
from src.infrastructure.logging.config import get_logger

router = APIRouter()
logger = get_logger(__name__)

class SQLQueryRequest(BaseModel):
    query: str

class SQLQueryResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    row_count: int

@router.post(
    "/sql",
    response_model=SQLQueryResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_api_key)]
)
async def execute_sql_query(request: SQLQueryRequest):
    """
    Executa consulta SQL diretamente no InfluxDB v3.
    
    Exemplos de consultas:
    - SELECT * FROM sensor_readings WHERE time > now() - interval '1 hour'
    - SELECT sensor_id, AVG(temperature) FROM sensor_readings GROUP BY sensor_id
    - SELECT * FROM sensor_readings WHERE sensor_id = 'sensor-001' ORDER BY time DESC LIMIT 10
    """
    logger.info(f"Executing SQL query: {request.query}")
    
    if not get_client():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="InfluxDB v3 connection unavailable"
        )
    
    try:
        # Executa a consulta SQL
        result = query_sensor_data_sql(request.query)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Query execution failed"
            )
        
        # Converte o resultado para lista de dicionários
        rows = []
        if hasattr(result, 'to_pandas'):
            # Se retornou um DataFrame pandas
            df = result.to_pandas()
            rows = df.to_dict('records')
        elif hasattr(result, '__iter__'):
            # Se retornou um iterável
            rows = list(result)
        else:
            rows = [result] if result else []
        
        return SQLQueryResponse(
            query=request.query,
            results=rows,
            row_count=len(rows)
        )
        
    except Exception as e:
        logger.error(f"SQL query failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Query execution error: {str(e)}"
        )

@router.get(
    "/recent",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_api_key)]
)
async def get_recent_sensor_data(limit: int = 50):
    """
    Busca os dados de sensores mais recentes (últimas 24 horas).
    """
    sql_query = f"""
    SELECT 
        time,
        sensor_id,
        client_ip,
        temperature,
        humidity,
        pressure
    FROM sensor_readings 
    WHERE time > now() - interval '24 hours'
    ORDER BY time DESC 
    LIMIT {limit}
    """
    
    request = SQLQueryRequest(query=sql_query)
    return await execute_sql_query(request)

@router.get(
    "/sensor/{sensor_id}/latest",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_api_key)]
)
async def get_sensor_latest_data(sensor_id: str, limit: int = 10):
    """
    Busca os dados mais recentes de um sensor específico.
    """
    sql_query = f"""
    SELECT 
        time,
        temperature,
        humidity,
        pressure,
        client_ip
    FROM sensor_readings 
    WHERE sensor_id = '{sensor_id}'
    ORDER BY time DESC 
    LIMIT {limit}
    """
    
    request = SQLQueryRequest(query=sql_query)
    return await execute_sql_query(request)
