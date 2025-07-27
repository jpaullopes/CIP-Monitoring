# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError, ArgumentError, IntegrityError
from typing import Optional

from .config import DATABASE_URL, app_state
from .models import Base
from .logger_config import setup_logger

logger = setup_logger(__name__)

# --- Global Variables for Database (will be initialized on startup) ---
engine = None
SessionLocal = None

def initialize_database():
    """Initialize database connection and create tables."""
    global engine, SessionLocal
    
    if not DATABASE_URL:
        app_state.db_is_connected = False
        logger.warning("DATABASE_URL not defined. The application will continue without saving data.")
        return

    try:
        logger.info("Configuring the database engine...")
        engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        logger.info("Attempting to connect to the database...")
        with engine.connect() as connection:
            logger.info("Database connection established successfully.")

            # Table creation logic - safe for multiple workers
            try:
                logger.info("Ensuring database tables are created...")
                Base.metadata.create_all(bind=engine)
                logger.info("Tables are ready.")
            except IntegrityError:
                logger.warning("Tables already exist, which is normal in a multi-worker environment. Continuing...")
                pass  # Ignore error, table was already created by another worker.

        app_state.db_is_connected = True

    except (OperationalError, ArgumentError) as e:
        app_state.db_is_connected = False
        logger.error("STARTUP ERROR: Could not configure or connect to the database.")
        logger.warning("The application will continue to receive data, but NOTHING will be saved.")
        if isinstance(e, ArgumentError):
            logger.error("Error detail: The provided database URL is invalid.")
        else:
            logger.error("Error detail: Connection to the server failed.")

    except Exception as e:
        app_state.db_is_connected = False
        logger.exception(f"An unexpected error occurred during startup: {e}")

# --- Dependency to get Database Session ---
def get_db():
    """Dependency to get database session."""
    if not app_state.db_is_connected or not SessionLocal:
        yield None
        return

    db = SessionLocal()
    try:
        yield db
    finally:
        if db and app_state.db_is_connected:
            try:
                db.close()
            except OperationalError:
                pass
