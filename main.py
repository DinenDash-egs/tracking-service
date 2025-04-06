from motor.motor_asyncio import AsyncIOMotorClient
import uuid
import os
from fastapi import HTTPException
from models import DeliveryRequest, DeliveryUpdate, DeliveryResponse, DeliveryStatus
import geocoder
from datetime import datetime
import pika
import time
import json

# Configuração do MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/trackingdb")
client = AsyncIOMotorClient(MONGO_URI)
db = client.trackingdb
deliveries_collection = db["deliveries"]

# Configuração do RabbitMQ
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = 5672

QUEUE_NAME = "geolocation"

def get_location():
    """Retrieve approximate geolocation data of the machine."""
    g = geocoder.ip("me")
    if g.ok:
        return {
            "latitude": g.latlng[0],
            "longitude": g.latlng[1],
            "city": g.city,
            "country": g.country,
            "ip": g.ip,
            "timestamp": datetime.utcnow().isoformat()
        }
    return {"error": "Unable to retrieve location"}

def send_message_to_queue(data: dict):
    """Send JSON data to RabbitMQ queue with retry logic."""
    connection = None
    retries = 5
    while retries > 0:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
            )
            break
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ is not ready yet. Retrying in 5 seconds...")
            time.sleep(5)
            retries -= 1

    if connection is None:
        raise Exception("Failed to connect to RabbitMQ after multiple retries.")

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    message = json.dumps(data)
    channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=message)
    connection.close()

# Criar um novo registo de entrega
async def create_delivery(delivery: DeliveryRequest):
    tracking_id = str(uuid.uuid4())
    delivery_data = {
        "tracking_id": tracking_id,
        "order_id": delivery.order_id,
        "customer_name": delivery.customer_name,
        "inicial_address": delivery.inicial_address,
        "delivery_address": delivery.delivery_address,
        "estimated_delivery_time": delivery.estimated_delivery_time,
        "status": delivery.status.value
    }
    await deliveries_collection.insert_one(delivery_data)
    return DeliveryResponse(**delivery_data)

# Atualizar status da entrega
async def update_delivery_status(tracking_id: str, update: DeliveryUpdate):
    result = await deliveries_collection.find_one({"tracking_id": tracking_id})
    if not result:
        raise HTTPException(status_code=404, detail="Delivery not found")

    await deliveries_collection.update_one(
        {"tracking_id": tracking_id},
        {"$set": {"status": update.status.value}}
    )
    return {"message": f"Delivery {tracking_id} updated to {update.status.value}"}

# Obter status de uma entrega específica
async def get_delivery_status(tracking_id: str):
    delivery = await deliveries_collection.find_one({"tracking_id": tracking_id})
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return DeliveryResponse(**delivery)

# Listar entregas com filtros opcionais
async def get_deliveries(status: DeliveryStatus = None, limit: int = 10, offset: int = 0):
    query = {}
    if status:
        query["status"] = status.value

    deliveries_cursor = deliveries_collection.find(query).skip(offset).limit(limit)
    deliveries = await deliveries_cursor.to_list(length=limit)
    
    return [DeliveryResponse(**delivery) for delivery in deliveries]

# Deletar um registo de entrega
async def delete_delivery(tracking_id: str):
    result = await deliveries_collection.delete_one({"tracking_id": tracking_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return {"message": f"Delivery {tracking_id} deleted successfully"}
