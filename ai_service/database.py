
from sqlmodel import SQLModel, create_engine, Session
import os
import sys

def _get_app_data_dir() -> str:
    if sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/StockNewsPro")
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
        return os.path.join(base, "StockNewsPro")
    return os.path.expanduser("~/.local/share/stock-news-pro")

# Ensure data directory exists
DATA_DIR = _get_app_data_dir()
os.makedirs(DATA_DIR, exist_ok=True)

SQLITE_FILE_NAME = "stock_news.db"
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, SQLITE_FILE_NAME)}"

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

def init_db():
    # Import models here to ensure they are registered with SQLModel.metadata
    from ai_service.models import Transaction
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
