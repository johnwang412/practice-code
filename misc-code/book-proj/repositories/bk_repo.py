from typing import Optional

from data import bk_data
from entities import bk_entity


class BookRepo:
    def __init__(self, db: bk_data.MockDB):
        self.db = db

    def rehydrate_book(self, book_uuid: str, version: Optional[str] = None) -> dict:
        bk_dict: dict = self.db.get_book(book_uuid, version=version)
        bk: bk_entity.Book = bk_entity.Book(
            uuid=bk_dict["uuid"],
            title=bk_dict["title"],
            author_uuid=bk_dict["author_uuid"],
            version=bk_dict["version"],
        )
        pages = self.db.get_pages(book_uuid)
        bk.set_pages(pages)
        return bk


def get_book_repo(db: bk_data.MockDB):
    return BookRepo(db)