import os
import flask
from influxdb_client_3 import InfluxDBClient3, Point
from dotenv import load_dotenv
import datetime

# Carregando variáveis de ambiente do .env
load_dotenv()

INFLUX_HOST = os.getenv("INFLUX_HOST", "http://localhost:8181")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_DATABASE = os.getenv("INFLUX_DATABASE", "sensores")

# Iniciando a aplicação Flask
app = flask.Flask(__name__)

# Cliente de conexão com o InfluxDB v3
try: 
    client = InfluxDBClient3(host=INFLUX_HOST, token=INFLUX_TOKEN, database=INFLUX_DATABASE)
    print(f"Conectado ao InfluxDB v3 em {INFLUX_HOST}")
except Exception as e:
    print(f"Erro ao conectar ao InfluxDB: {e}")
    client = None

# Rota para receber dados do sensor
@app.route('/api/dados-sensor', methods=['POST'])
def receber_dados():
    dados = flask.request.get_json()
    print(f"Dados recebido: {dados}")

    # Criando ponto de dados para InfluxDB v3
    try:
        if not client:
            return flask.jsonify({"error": "InfluxDB não conectado"}), 500
            
        # Para InfluxDB v3, usar Point da biblioteca influxdb_client_3
        ponto = Point("manitoramento_cip") \
            .tag("local", dados.get("id_sensor")) \
            .tag("cip_id", dados.get("cip_id", "default")) \
            .tag("status_cip", dados.get("status_cip", "active")) \
            .field("temperature", float(dados.get("temperature"))) \
            .field("pressure", float(dados.get("pressure"))) \
            .field("concentration", float(dados.get("concentration"))) \
            .time(datetime.datetime.now(datetime.timezone.utc))

        # Escrevendo ponto no InfluxDB v3
        client.write(record=ponto)
        print(f"Dados escritos: {dados}")

        return flask.jsonify({"status": "success"}), 201

    except Exception as e:
        print(f"Erro ao criar ponto de dados: {e}")
        return flask.jsonify({"error": "Erro ao processar os dados"}), 500

# Rodando a aplicação Flask 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)