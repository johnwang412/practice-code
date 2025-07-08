import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from models import Base

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def get_test_db():
    """
    Get test database session.
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_test_tables():
    """
    Create all tables for testing.
    """
    Base.metadata.create_all(bind=test_engine)


def drop_test_tables():
    """
    Drop all test tables.
    """
    Base.metadata.drop_all(bind=test_engine)
