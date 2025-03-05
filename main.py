from motor.motor_asyncio import AsyncIOMotorClient
import os
from fastapi import HTTPException

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/tracking_db")
client = AsyncIOMotorClient(MONGO_URI)
db = client.tracking_db
deliveries_collection = db["deliveries"]

async def init_db():
    """Inicializa a base de dados e verifica a conexão"""
    try:
        await client.server_info()
        print("Conectado ao MongoDB!")
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")

async def register_delivery(order_id: str, status: str):
    """Registra uma nova entrega na base de dados"""
    delivery_data = {"order_id": order_id, "status": status}
    await deliveries_collection.insert_one(delivery_data)
    return {"message": "Delivery registered successfully"}

async def update_delivery_status(order_id: str, status: str):
    """Atualiza o status de uma entrega"""
    result = await deliveries_collection.update_one({"order_id": order_id}, {"$set": {"status": status}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return {"message": f"Delivery {order_id} updated to {status}"}

async def get_delivery_status(order_id: str):
    """Obtém o status de uma entrega"""
    delivery = await deliveries_collection.find_one({"order_id": order_id})
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return {"order_id": order_id, "status": delivery["status"]}
