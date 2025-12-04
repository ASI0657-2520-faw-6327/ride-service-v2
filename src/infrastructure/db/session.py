from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import settings
from src.infrastructure.db.base import Base


engine = create_engine(
    settings.DATABASE_URL,
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Session:
    return SessionLocal()


def init_db() -> None:
    """
    Crea las tablas en la base de datos (solo para dev; en prod usar migraciones).
    """
    # Asegúrate de que los modelos están importados antes de crear las tablas
    import src.infrastructure.db.models  # noqa: F401

    Base.metadata.create_all(bind=engine)

