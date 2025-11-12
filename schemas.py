"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Example schemas (keep for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# FESdmiT App Schemas

class Event(BaseModel):
    """
    Event collection schema
    Collection name: "event"
    """
    title: str = Field(..., description="Event title")
    description: Optional[str] = Field(None, description="Event description")
    date: datetime = Field(..., description="Event date and time (ISO)")
    location: str = Field(..., description="Venue or location")
    capacity: Optional[int] = Field(None, ge=1, description="Max registrations allowed")
    tags: Optional[List[str]] = Field(default=None, description="Tags for filtering")

class Registration(BaseModel):
    """
    Registration collection schema
    Collection name: "registration"
    """
    event_id: str = Field(..., description="ID of the event being registered for")
    name: str = Field(..., description="Student full name")
    email: EmailStr = Field(..., description="Student email")
    department: Optional[str] = Field(None, description="Department or program")
    year: Optional[str] = Field(None, description="Year of study")
    roll_no: Optional[str] = Field(None, description="Roll number / Student ID")
    phone: Optional[str] = Field(None, description="Contact number")

# Add more schemas as needed
