from typing import Optional


class MockDB:
    def __init__(self):
        self.books = {}
        self.pages = {}

    def get_book(self, book_uuid: str, version: Optional[str] = None) -> dict:
        return {
            "uuid": book_uuid,
            "title": "Mock Book Title",
            "author_uuid": "author-uuid",
            "version": version or None,
        }

    def get_pages(self, book_uuid: str) -> list[dict]:
        return [
            {
                "uuid": f"page-{i}",
                "book_uuid": book_uuid,
                "page_number": i,
                "content_json": '{"text": "Bunny is cute", "x-position": "120", "y-position": "30"}',
            }
            for i in range(1, 11)
        ]


def get_mock_db():
    return MockDB()
