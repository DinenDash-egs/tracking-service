# api.py
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- Add this import
from models import (
    DeliveryRequest, DeliveryUpdate, DeliveryResponse, DeliveryStatus,
    LocationResponse, SendLocationResponse
)
from main import (
    get_location, create_delivery, update_delivery_status,
    get_delivery_status, get_deliveries, delete_delivery
)

app = FastAPI(
    title="Tracking API",
    version="1.0",
    description="This API allows tracking deliveries, retrieving real-time status updates, and managing deliveries efficiently."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/v1")


@router.post("/deliveries", response_model=DeliveryResponse, summary="Create a new delivery")
async def create_delivery_endpoint(delivery: DeliveryRequest):
    """Creates a new delivery record, assigning a unique tracking ID and storing relevant package details."""
    return await create_delivery(delivery)


@router.put("/deliveries/{tracking_id}", response_model=dict, summary="Update delivery status")
async def update_delivery_status_endpoint(tracking_id: str, update: DeliveryUpdate):
    """Updates the status of an existing delivery, marking changes in the delivery tracking system."""
    return await update_delivery_status(tracking_id, update)


@router.get("/deliveries/{tracking_id}", response_model=DeliveryResponse, summary="Get delivery details")
async def get_delivery_status_endpoint(tracking_id: str):
    """Fetches the latest tracking details of a specific delivery."""
    return await get_delivery_status(tracking_id)


@router.get("/deliveries", response_model=list[DeliveryResponse], summary="Retrieve all deliveries")
async def get_deliveries_endpoint(status: DeliveryStatus = None, limit: int = 10, offset: int = 0):
    """
    Retrieves a paginated list of deliveries, optionally filtered by status.

    - `status`: (Optional) Filter deliveries by their current status.
    - `limit`: (Optional) Number of records to return per request (default: 10).
    - `offset`: (Optional) Number of records to skip for pagination.
    """
    return await get_deliveries(status, limit, offset)


@router.delete("/deliveries/{tracking_id}", response_model=dict, summary="Delete a delivery record")
async def delete_delivery_endpoint(tracking_id: str):
    """Removes a specific delivery record from the system based on its tracking ID."""
    return await delete_delivery(tracking_id)


@router.get("/location", response_model=LocationResponse, summary="Obtain system location")
async def get_location_endpoint():
    """Retrieves the approximate geolocation of the current system based on its external IP address."""
    return get_location()


app.include_router(router)


@app.get("/", summary="Health Check")
async def root():
    """Returns a simple health check message confirming the API is running."""
    return {"message": "Tracking Service is running"}
