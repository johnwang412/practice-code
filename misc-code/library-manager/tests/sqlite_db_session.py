"""
TODO: incorporate this later
"""
from sqlalchemy import create_engine
from sqlalchemy import orm

from app.models.base import Base


_SESSION_FACTORY = None
_ENGINE = None


def get_rw_session_from_clean_db():
    _init_test_database_if_none()
    _reset_database_schema()
    return _SESSION_FACTORY()


def _reset_database_schema():
    """Clean up existing in memory sqlite database"""
    global _ENGINE
    if _ENGINE:
        # https://docs.sqlalchemy.org/en/13/orm/session_api.html
        # - #sqlalchemy.orm.session.close_all_sessions
        orm.session.close_all_sessions()

        Base.metadata.drop_all(_ENGINE)
        Base.metadata.create_all(_ENGINE)


def _init_test_database_if_none():
    global _ENGINE
    global _SESSION_FACTORY

    if not _SESSION_FACTORY:
        echo_sql_queries = False
        _ENGINE = create_engine('sqlite://', echo=echo_sql_queries)

        _SESSION_FACTORY = orm.sessionmaker(bind=_ENGINE, expire_on_commit=False)