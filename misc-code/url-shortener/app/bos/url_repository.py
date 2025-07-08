from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import URLMapping


class URLRepository:
    """
    Repository class for handling URL mapping database operations.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_url_mapping(self, original_url: str, short_code: str) -> Optional[URLMapping]:
        """
        Create a new URL mapping in the database.
        
        Args:
            original_url: The original URL to be shortened
            short_code: The generated short code
            
        Returns:
            URLMapping object if successful, None if short_code already exists
        """
        try:
            url_mapping = URLMapping(
                original_url=original_url,
                short_code=short_code
            )
            self.db.add(url_mapping)
            self.db.commit()
            self.db.refresh(url_mapping)
            return url_mapping
        except IntegrityError:
            # Short code already exists
            self.db.rollback()
            return None
    
    def get_url_by_short_code(self, short_code: str) -> Optional[URLMapping]:
        """
        Retrieve a URL mapping by its short code.
        
        Args:
            short_code: The short code to look up
            
        Returns:
            URLMapping object if found, None otherwise
        """
        return self.db.query(URLMapping).filter(
            URLMapping.short_code == short_code
        ).first()
    
    def get_url_by_original_url(self, original_url: str) -> Optional[URLMapping]:
        """
        Retrieve a URL mapping by its original URL.
        
        Args:
            original_url: The original URL to look up
            
        Returns:
            URLMapping object if found, None otherwise
        """
        return self.db.query(URLMapping).filter(
            URLMapping.original_url == original_url
        ).first()
    
    def short_code_exists(self, short_code: str) -> bool:
        """
        Check if a short code already exists in the database.
        
        Args:
            short_code: The short code to check
            
        Returns:
            True if exists, False otherwise
        """
        return self.db.query(URLMapping).filter(
            URLMapping.short_code == short_code
        ).first() is not None
    
    def get_all_mappings(self, limit: int = 100, offset: int = 0) -> list[URLMapping]:
        """
        Get all URL mappings with pagination.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of URLMapping objects
        """
        return self.db.query(URLMapping).offset(offset).limit(limit).all()
