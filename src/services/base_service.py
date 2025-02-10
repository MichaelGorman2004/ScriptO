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

from typing import Generic, TypeVar, Type, Optional
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import HTTPException

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all services providing common CRUD operations and utility methods.
    
    Attributes:
        model: The SQLAlchemy model class
        db: Database session
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    async def get(self, id: UUID) -> Optional[ModelType]:
        """
        Retrieve a single record by ID.
        
        Args:
            id: UUID of the record to retrieve
            
        Returns:
            The found record or None
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    async def get_all(self, skip: int = 0, limit: int = 100):
        """
        Retrieve multiple records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of records
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    async def create(self, schema: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        
        Args:
            schema: Pydantic schema containing the data for creation
            
        Returns:
            The created record
        """
        db_item = self.model(**schema.model_dump())
        self.db.add(db_item)
        try:
            self.db.commit()
            self.db.refresh(db_item)
            return db_item
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    
    async def update(self, id: UUID, schema: UpdateSchemaType) -> Optional[ModelType]:
        """
        Update an existing record.
        
        Args:
            id: UUID of the record to update
            schema: Pydantic schema containing the update data
            
        Returns:
            The updated record or None if not found
        """
        db_item = await self.get(id)
        if not db_item:
            return None
            
        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
            
        try:
            self.db.commit()
            self.db.refresh(db_item)
            return db_item
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    
    async def delete(self, id: UUID) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: UUID of the record to delete
            
        Returns:
            True if deleted, False if not found
        """
        db_item = await self.get(id)
        if not db_item:
            return False
            
        try:
            self.db.delete(db_item)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e)) 