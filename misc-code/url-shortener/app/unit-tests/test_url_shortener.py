import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.url_api import app
from database import get_db
from test_database import get_test_db, create_test_tables, drop_test_tables
from logic.shorten_url import create_short_url, get_original_url
from bos.url_repository import URLRepository


# Override the dependency
app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """
    Create a fresh database for each test.
    """
    create_test_tables()
    db = next(get_test_db())
    yield db
    db.close()
    drop_test_tables()


class TestURLShortener:
    """Test cases for URL shortener functionality."""
    
    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    
    def test_shorten_url_endpoint(self, test_db: Session):
        """Test the URL shortening endpoint."""
        test_url = "https://www.example.com"
        
        response = client.put("/shorten", json={"url": test_url})
        
        assert response.status_code == 200
        data = response.json()
        assert "original_url" in data
        assert "short_code" in data
        assert "short_url" in data
        assert data["original_url"] == test_url
        assert len(data["short_code"]) == 8
        assert data["short_url"].endswith(data["short_code"])
    
    def test_shorten_url_duplicate(self, test_db: Session):
        """Test that shortening the same URL returns the same short code."""
        test_url = "https://www.example.com"
        
        # First request
        response1 = client.put("/shorten", json={"url": test_url})
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Second request with same URL
        response2 = client.put("/shorten", json={"url": test_url})
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Should return the same short code
        assert data1["short_code"] == data2["short_code"]
    
    def test_redirect_endpoint(self, test_db: Session):
        """Test the redirect endpoint."""
        test_url = "https://www.example.com"
        
        # First create a short URL
        response = client.put("/shorten", json={"url": test_url})
        assert response.status_code == 200
        short_code = response.json()["short_code"]
        
        # Test redirect
        redirect_response = client.get(f"/{short_code}", follow_redirects=False)
        assert redirect_response.status_code == 301
        assert redirect_response.headers["location"] == test_url
    
    def test_redirect_not_found(self, test_db: Session):
        """Test redirect with non-existent short code."""
        response = client.get("/nonexistent", follow_redirects=False)
        assert response.status_code == 404
        assert "Short URL not found" in response.json()["detail"]
    
    def test_invalid_url(self, test_db: Session):
        """Test shortening an invalid URL."""
        response = client.put("/shorten", json={"url": "not-a-valid-url"})
        assert response.status_code == 422  # Validation error


class TestBusinessLogic:
    """Test cases for business logic functions."""
    
    def test_create_short_url(self, test_db: Session):
        """Test creating a short URL mapping."""
        test_url = "https://www.example.com"
        
        mapping = create_short_url(test_url, test_db)
        
        assert mapping is not None
        assert mapping.original_url == test_url.lower()
        assert len(mapping.short_code) == 8
        assert mapping.created_at is not None
    
    def test_get_original_url(self, test_db: Session):
        """Test retrieving original URL by short code."""
        test_url = "https://www.example.com"
        
        # Create mapping
        mapping = create_short_url(test_url, test_db)
        assert mapping is not None
        
        # Retrieve original URL
        retrieved_url = get_original_url(mapping.short_code, test_db)
        assert retrieved_url == test_url.lower()
    
    def test_get_original_url_not_found(self, test_db: Session):
        """Test retrieving non-existent short code."""
        result = get_original_url("nonexist", test_db)
        assert result is None


class TestRepository:
    """Test cases for URL repository."""
    
    def test_create_url_mapping(self, test_db: Session):
        """Test creating URL mapping in repository."""
        repo = URLRepository(test_db)
        test_url = "https://www.example.com"
        short_code = "abc12345"
        
        mapping = repo.create_url_mapping(test_url, short_code)
        
        assert mapping is not None
        assert mapping.original_url == test_url
        assert mapping.short_code == short_code
    
    def test_get_url_by_short_code(self, test_db: Session):
        """Test retrieving URL mapping by short code."""
        repo = URLRepository(test_db)
        test_url = "https://www.example.com"
        short_code = "abc12345"
        
        # Create mapping
        created_mapping = repo.create_url_mapping(test_url, short_code)
        assert created_mapping is not None
        
        # Retrieve mapping
        retrieved_mapping = repo.get_url_by_short_code(short_code)
        assert retrieved_mapping is not None
        assert retrieved_mapping.original_url == test_url
        assert retrieved_mapping.short_code == short_code
    
    def test_short_code_exists(self, test_db: Session):
        """Test checking if short code exists."""
        repo = URLRepository(test_db)
        test_url = "https://www.example.com"
        short_code = "abc12345"
        
        # Should not exist initially
        assert not repo.short_code_exists(short_code)
        
        # Create mapping
        repo.create_url_mapping(test_url, short_code)
        
        # Should exist now
        assert repo.short_code_exists(short_code)
