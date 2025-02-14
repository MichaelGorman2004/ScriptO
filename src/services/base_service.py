"""
Base Service Class

This module provides the foundation for all service classes in the application.
It includes common functionality, error handling, and utility methods that will
be shared across different services.

Key Features:
- Common error handling
- Database session management
- Logging setup
- Base CRUD operations
"""

from typing import Generic, TypeVar, Type, Optional, List
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.utils.logging import logger

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all services providing common CRUD operations and utility methods.
    
    Attributes:
        model: The SQLAlchemy model class
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize service with model class.
        Database session will be injected per request.
        """
        self.model = model
    
    async def get(self, db: Session, id: UUID) -> Optional[ModelType]:
        """
        Retrieve a single record by ID.
        
        Args:
            id: UUID of the record to retrieve
            
        Returns:
            The found record or None
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    async def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Retrieve multiple records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of records
        """
        return db.query(self.model).offset(skip).limit(limit).all()
    
    async def create(
        self,
        db: Session,
        schema: CreateSchemaType
    ) -> ModelType:
        """
        Create a new record.
        
        Args:
            schema: Pydantic schema containing the data for creation
            
        Returns:
            The created record
        """
        try:
            db_item = self.model(**schema.model_dump())
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item
        except Exception as e:
            db.rollback()
            logger.error(f"Create error in {self.__class__.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    
    async def update(
        self,
        db: Session,
        id: UUID,
        schema: UpdateSchemaType
    ) -> Optional[ModelType]:
        """
        Update an existing record.
        
        Args:
            id: UUID of the record to update
            schema: Pydantic schema containing the update data
            
        Returns:
            The updated record or None if not found
        """
        try:
            db_item = await self.get(db, id)
            if not db_item:
                return None
                
            update_data = schema.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_item, field, value)
                
            db.commit()
            db.refresh(db_item)
            return db_item
        except Exception as e:
            db.rollback()
            logger.error(f"Update error in {self.__class__.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    
    async def delete(self, db: Session, id: UUID) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: UUID of the record to delete
            
        Returns:
            True if deleted, False if not found
        """
        try:
            db_item = await self.get(db, id)
            if not db_item:
                return False
                
            db.delete(db_item)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Delete error in {self.__class__.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e)) 