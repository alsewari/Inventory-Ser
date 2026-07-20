from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Inventory
from database import test_connection
import service


app = FastAPI(
    title="Inventory Service API",
    description="Inventory Microservice for Order Product System",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    await test_connection()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Inventory Service is running"
    }


@app.post("/api/inventory", status_code=201)
async def create_inventory(inventory: Inventory):
    created_item = await service.create_inventory(inventory)

    if created_item is None:
        raise HTTPException(
            status_code=400,
            detail="Inventory record already exists for this product."
        )

    return created_item


@app.get("/api/inventory")
async def get_all_inventory():
    return await service.get_all_inventory()


@app.get("/api/inventory/{product_id}")
async def get_inventory_by_product_id(product_id: str):
    item = await service.get_inventory_by_product_id(product_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found."
        )

    return item


@app.put("/api/inventory/{product_id}")
async def update_inventory(
    product_id: str,
    inventory: Inventory
):
    updated_item = await service.update_inventory(
        product_id,
        inventory
    )

    if updated_item is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found."
        )

    return updated_item


@app.get("/api/inventory/{product_id}/available/{quantity}")
async def check_availability(
    product_id: str,
    quantity: int
):
    available = await service.check_availability(
        product_id,
        quantity
    )

    if available is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found."
        )

    return {
        "product_id": product_id,
        "requested_quantity": quantity,
        "available": available
    }


@app.post("/api/inventory/{product_id}/reduce/{quantity}")
async def reduce_stock(
    product_id: str,
    quantity: int
):
    result = await service.reduce_stock(
        product_id,
        quantity
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found."
        )

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available."
        )

    return result


@app.delete("/api/inventory/{product_id}")
async def delete_inventory(product_id: str):
    deleted = await service.delete_inventory(product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found."
        )

    return {
        "message": "Inventory item deleted successfully."
    }