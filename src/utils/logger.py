import logging
import json
import os
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(exist_ok=True)


class JSONFormatter(logging.Formatter):

    def format(self, record):
        try:
            msg = json.loads(record.getMessage())
        except (json.JSONDecodeError, TypeError):
            msg = {"message": record.getMessage()}

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            **msg
        }

        return json.dumps(entry)


def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = JSONFormatter()

    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler
    file_handler = logging.FileHandler(LOG_DIR / "financial_copilot.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
