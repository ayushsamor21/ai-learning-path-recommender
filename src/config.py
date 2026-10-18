import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

MONGODB_URI = os.getenv("MONGODB_URI", "").strip()
MONGODB_DB = os.getenv("MONGODB_DB", "learnpath").strip() or "learnpath"
LOCAL_DB_PATH = ROOT / "data" / ".local_db.json"


def mongo_uri_from_secrets(secrets) -> str:
    try:
        return str(secrets.get("MONGODB_URI", "") or "").strip()
    except Exception:
        return ""
