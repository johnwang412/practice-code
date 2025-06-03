from sqlalchemy import Column, Integer, String

from app.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.first_name} {self.last_name}')>"