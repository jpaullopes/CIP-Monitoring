# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Environment Variables ---
EXPECTED_API_KEY = os.getenv("API_KEY")
EXPECTED_API_KEY_WS = os.getenv("API_KEY_WS")

# InfluxDB Configuration
INFLUX_HOST = os.getenv("INFLUX_HOST", "http://localhost:8181")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_DATABASE = os.getenv("INFLUX_DATABASE", "sensores")

# WebSocket connection limits
MAX_WS_CONNECTIONS_PER_KEY_STR = os.getenv("MAX_WS_CONNECTIONS_PER_KEY")
MAX_WS_CONNECTIONS_PER_KEY: int = 0  # Default to 0 (unlimited)

try:
    if MAX_WS_CONNECTIONS_PER_KEY_STR:
        MAX_WS_CONNECTIONS_PER_KEY = int(MAX_WS_CONNECTIONS_PER_KEY_STR)
        if MAX_WS_CONNECTIONS_PER_KEY < 0:  # Ensures it's not negative
            MAX_WS_CONNECTIONS_PER_KEY = 0
except ValueError:
    MAX_WS_CONNECTIONS_PER_KEY = 0

# --- Global Application State ---
class AppState:
    """A simple class to hold the InfluxDB connection state."""
    def __init__(self):
        self.influx_is_connected: bool = False

app_state = AppState()
