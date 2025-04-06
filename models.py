# models.py
from __future__ import annotations
from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class DeliveryStatus(Enum):
    """Enumeration of possible delivery statuses."""
    pending = "pending"
    in_transit = "in_transit"
    delivered = "delivered"
    canceled = "canceled"


class DeliveryRequest(BaseModel):
    """Model representing a delivery request containing package details and destination."""
    order_id: str = Field(..., example="order123", description="Unique identifier for the order.")
    customer_name: str = Field(..., example="João Sousa", description="Name of the recipient.")
    address: str = Field(..., example="Rua Exemplo, 123, Lisboa", description="Full initial address where the package starts.")
    delivery_address: str = Field(..., example="Avenida Exemplo, 456, Porto", description="Full delivery destination address.")
    delivery_date: datetime = Field(..., example="2025-03-11T15:00:00Z", description="Date and time scheduled for delivery in UTC.")
    status: DeliveryStatus = Field(default=DeliveryStatus.pending, description="Current delivery status.")
    estimated_delivery_time: datetime = Field(..., example="2025-03-11T15:00:00Z", description="Estimated delivery time in UTC.")


class DeliveryUpdate(BaseModel):
    """Model for updating delivery status."""
    status: DeliveryStatus = Field(..., description="New status of the delivery.")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the latest status update.")


class DeliveryResponse(BaseModel):
    """Model representing the details of a delivery response."""
    tracking_id: str = Field(..., example="track123", description="Unique tracking identifier for the delivery.")
    order_id: str = Field(..., example="order123", description="Unique order identifier.")
    customer_name: str = Field(..., example="João Sousa", description="Name of the recipient.")
    inicial_address: str = Field(..., example="Rua Exemplo, 123, Lisboa", description="Initial address from where the delivery started.")
    delivery_address: str = Field(..., example="Avenida Exemplo, 456, Porto", description="Delivery destination address.")
    delivery_date: datetime = Field(..., example="2025-03-11T15:00:00Z", description="Scheduled delivery date and time in UTC.")
    status: DeliveryStatus = Field(..., description="Current status of the delivery.")
    last_updated: datetime = Field(..., description="Last update timestamp of the delivery status.")


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
