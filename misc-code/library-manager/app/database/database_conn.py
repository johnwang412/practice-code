from app.database.catalog_db import CatalogDB


def _db_session():
    # TODO: generate sqlalchemy session
    return None

def get_catalog_db():
    db_session = _db_session()
    return CatalogDB(db_session)