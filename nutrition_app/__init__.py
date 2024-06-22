import logging
import os
from pathlib import Path

database_path = Path(__file__).parent / "nutrition_app_database.db"

logger = logging.getLogger("nutrition_app")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

