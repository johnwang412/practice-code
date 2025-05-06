
class Page:
    def __init__(self, page_uuid, book_uuid, page_number: int, content_json: str):
        self.page_uuid = page_uuid
        self.book_uuid = book_uuid
        self.page_number = page_number
        self.content_json = content_json


class Book:
    def __init__(self, uuid: str, title: str, author_uuid: str, version: str):
        self.uuid = uuid
        self.title = title
        self.author_uuid = author_uuid
        self.version = version
        self.pages: list[Page] = []

    def __str__(self):
        ret = f"Book(title={self.title}, author_uuid={self.author_uuid}, version={self.version}, pages={len(self.pages)})"
        for page in self.pages:
            ret += f"\n  {page.page_number}: {page.content_json}"
        return ret

    def get_num_pages(self) -> int:
        return len(self.pages)

    def set_pages(self, pages: list[dict]):
        """
                "uuid": f"page-{i}",
                "book_uuid": book_uuid,
                "page_number": i,
                "content_json": '{"text": "Bunny is cute", "x-position": "120", "y-position": "30"}',
        """
        self.pages = [
            Page(
                page_uuid=page["uuid"],
                book_uuid=page["book_uuid"],
                page_number=page["page_number"],
                content_json=page["content_json"],
            )
            for page in pages
        ]