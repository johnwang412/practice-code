from contextlib import contextmanager

from sqlalchemy import create_engine, orm


# TODO: update to actual database
DATABASE_URL = "sqlite://"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = orm.sessionmaker(bind=engine, autocommit=False, autoflush=False)


@contextmanager
def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()