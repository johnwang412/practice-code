from app.models.books_orm import Book


class CatalogDB:
    def __init__(self, sqlalchemy_session):
        # SqlAlchemy session
        self.sqlalchemy_session = sqlalchemy_session

    def try_checkout(self, item_id, user_id) -> tuple[bool, str]:
        """
        :return: bool on whether checkout was successful and str with any errors
        """

        # TODO: ensure proper transaction handling and concurrency control
        book_orm: Book = self.sqlalchemy_session.get_one(Book, id=item_id)
        if book_orm.num_available <= book_orm.num_checked_out:
            return False, 'No copies available'

        # Checkout
        book_orm.num_checked_out += 1

        # TODO: add a checkout table entry

        return True, ''