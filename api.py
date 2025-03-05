from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from main import register_delivery, update_delivery_status, get_delivery_status, init_db

app = FastAPI()

router = APIRouter(prefix="/v1")

class DeliveryRequest(BaseModel):
    order_id: str
    status: str

@router.post("/deliveries", summary="Registar uma entrega", description="Registra uma nova entrega na base de dados.")
async def register_delivery_endpoint(delivery: DeliveryRequest):
    return await register_delivery(delivery.order_id, delivery.status)

@router.put("/deliveries/{order_id}", summary="Atualizar status da entrega", description="Atualiza o status de uma entrega específica.")
async def update_delivery_status_endpoint(order_id: str, delivery: DeliveryRequest):
    return await update_delivery_status(order_id, delivery.status)

@router.get("/deliveries/{order_id}", summary="Obter status da entrega", description="Obtém o status atual de uma entrega.")
async def get_delivery_status_endpoint(order_id: str):
    return await get_delivery_status(order_id)

app.include_router(router)
