import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from logging.handlers import RotatingFileHandler
from src.infrastructure.security.security_settings import get_security_settings
from src.infrastructure.logging.secure_logger_protocol import (
    SecureLogger,
    LogLevel,
    LogContext,
)


class SecureLoggerImpl:
    def __init__(self):
        self.settings = get_security_settings()
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("sensorflow_security")
        logger.propagate = False
        
        if logger.hasHandlers():
            return logger
        
        log_level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        logger.setLevel(log_level_map.get(self.settings.LOG_LEVEL, logging.INFO))
        
        if self.settings.ENABLE_JSON_LOGGING:

            try:
                log_dir = Path(self.settings.LOG_DIR)
                log_dir.mkdir(parents=True, exist_ok=True)
                
                log_file = log_dir / self.settings.LOG_FILE_NAME
                
                handler = RotatingFileHandler(
                    log_file,
                    maxBytes=self.settings.LOG_MAX_SIZE_BYTES,
                    backupCount=self.settings.LOG_BACKUP_COUNT,
                )
                formatter = logging.Formatter(
                    fmt="%(message)s",
                    datefmt="%Y-%m-%dT%H:%M:%S",
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            except (PermissionError, OSError) as e:
                print(f"Warning: Could not create log file, falling back to console: {e}")
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            logger.addHandler(handler)
        else:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _log_json(self, level: LogLevel, data: dict) -> None:
        data["timestamp"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        data["level"] = level.value
        
        if level == LogLevel.DEBUG:
            self.logger.debug(json.dumps(data))
        elif level == LogLevel.INFO:
            self.logger.info(json.dumps(data))
        elif level == LogLevel.WARNING:
            self.logger.warning(json.dumps(data))
        elif level == LogLevel.ERROR:
            self.logger.error(json.dumps(data))
        elif level == LogLevel.CRITICAL:
            self.logger.critical(json.dumps(data))
    
    def log_request(
        self,
        level: LogLevel,
        message: str,
        context: LogContext,
    ) -> None:
        data = {
            "message": message,
            **context.to_dict(),
        }
        self._log_json(level, data)
    
    def log_authentication_failure(
        self,
        reason: str,
        device_id: str | None = None,
    ) -> None:
        data = {
            "message": "Authentication failure",
            "reason": reason,
        }
        if device_id:
            data["device_id"] = device_id
        
        self._log_json(LogLevel.WARNING, data)
    
    def log_rate_limit_exceeded(
        self,
        device_id: str,
        requests_made: int,
        limit: int,
    ) -> None:
        data = {
            "message": "Rate limit exceeded",
            "device_id": device_id,
            "requests_made": requests_made,
            "limit": limit,
        }
        self._log_json(LogLevel.WARNING, data)
    
    def log_payload_validation_failure(
        self,
        device_id: str,
        reason: str,
        size_bytes: int | None = None,
    ) -> None:
        data = {
            "message": "Payload validation failure",
            "device_id": device_id,
            "reason": reason,
        }
        if size_bytes is not None:
            data["size_bytes"] = size_bytes
        
        self._log_json(LogLevel.WARNING, data)
    
    def log_sensor_data_processed(
        self,
        device_id: str,
        latency_ms: float,
    ) -> None:
        data = {
            "message": "Sensor data processed",
            "device_id": device_id,
            "latency_ms": latency_ms,
        }
        self._log_json(LogLevel.INFO, data)
