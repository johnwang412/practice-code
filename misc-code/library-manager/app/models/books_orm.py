from sqlalchemy import Column, Integer, String, ForeignKey

from app.models.base import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)
    isbn = Column(String, nullable=False)
    num_available = Column(Integer, nullable=False)
    num_checked_out = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Book(id={self.id}, author='{self.author}', title='{self.title}')>"