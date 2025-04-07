# models.py
from __future__ import annotations
from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class DeliveryStatus(str, Enum):
    pending = "pending"
    in_transit = "in_transit"
    delivered = "delivered"
    cancelled = "cancelled"


class DeliveryRequest(BaseModel):
    order_id: str
    customer_name: str
    address: str                     # User-selected location
    restaurant_address: str          # Placeholder for now
    delivery_date: datetime
    estimated_delivery_time: datetime
    status: DeliveryStatus

class DeliveryUpdate(BaseModel):
    """Model for updating delivery status."""
    status: DeliveryStatus = Field(..., description="New status of the delivery.")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the latest status update.")


class DeliveryResponse(BaseModel):
    tracking_id: str
    order_id: str
    customer_name: str
    address: str
    restaurant_address: str
    delivery_date: Optional[datetime] = None
    estimated_delivery_time: datetime
    status: DeliveryStatus
    last_updated: Optional[datetime] = None

class LocationResponse(BaseModel):
    """Model for representing location details obtained from the system."""
    latitude: Optional[float] = Field(None, example=38.7169, description="Latitude coordinate.")
    longitude: Optional[float] = Field(None, example=-9.1399, description="Longitude coordinate.")
    city: Optional[str] = Field(None, example="Lisboa", description="City of the detected location.")
    country: Optional[str] = Field(None, example="Portugal", description="Country of the detected location.")
    ip: Optional[str] = Field(None, example="192.168.1.1", description="IP address used to determine the location.")
    timestamp: Optional[datetime] = Field(None, example="2025-03-11T12:00:00Z", description="Timestamp when the location was retrieved.")


class SendLocationResponse(BaseModel):
    """Model representing a response when location data is sent."""
    status: str = Field(..., example="success", description="Status of the location data transmission.")
    data: LocationResponse = Field(..., description="Detailed location data retrieved.")
