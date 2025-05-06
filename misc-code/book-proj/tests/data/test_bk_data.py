import pytest

from data import bk_data


class TestBasic:
    """Using a class here just to test out pytest functionality."""
    @pytest.mark.parametrize(
        "book_uuid, version, expected",
        [
            ("book-uuid", "1.0", {"uuid": "book-uuid", "title": "Mock Book Title", "author_uuid": "author-uuid", "version": "1.0"}),
            ("book-uuid", None, {"uuid": "book-uuid", "title": "Mock Book Title", "author_uuid": "author-uuid", "version": None}),
        ],
    )
    def test_get_book(self, book_uuid, version, expected):
        db = bk_data.get_mock_db()
        book = db.get_book(book_uuid, version)
        assert book == expected

    def test_get_db(self):
        db = bk_data.get_mock_db()
        assert db is not None
