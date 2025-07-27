# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Environment Variables ---
EXPECTED_API_KEY = os.getenv("API_KEY")
EXPECTED_API_KEY_WS = os.getenv("API_KEY_WS")
DATABASE_URL = os.getenv("DATABASE_URL")

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
    """A simple class to hold the database connection state."""
    def __init__(self):
        self.db_is_connected: bool = False

app_state = AppState()
