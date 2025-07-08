from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class URLMapping(Base):
    """
    Model for storing URL mappings between original URLs and short codes.
    """
    __tablename__ = "url_mappings"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(2048), nullable=False)
    short_code = Column(String(8), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Add index for faster lookups by short_code
    __table_args__ = (
        Index('idx_short_code', 'short_code'),
    )

    def __repr__(self):
        return f"<URLMapping(id={self.id}, short_code='{self.short_code}', original_url='{self.original_url}')>"
