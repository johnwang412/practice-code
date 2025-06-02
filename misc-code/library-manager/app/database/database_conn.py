from app.database.catalog_db import CatalogDBConn


def get_catalog_db_conn():
    return CatalogDBConn()