import logging
import os
from pathlib import Path

products_dir = Path(__file__).parent / "products_db"


logger = logging.getLogger("nutrition_app")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
