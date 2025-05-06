import pytest

from repositories import bk_repo
from data import bk_data


def test_rehydrate_book():
    mock_db = bk_data.get_mock_db()
    book_repo = bk_repo.get_book_repo(mock_db)

    book_uuid = "book-uuid"
    version = "1.0"
    book = book_repo.rehydrate_book(book_uuid, version=version)
    assert book.uuid == book_uuid
    assert book.version == version
    assert book.get_num_pages() == 10