from datetime import datetime, timezone

from database import inventory_collection
from models import Inventory


def inventory_serializer(item: dict) -> dict:
    return {
        "id": str(item.get("_id", "")),
        "product_id": item.get("product_id", ""),
        "product_name": item.get("product_name", ""),
        "stock_quantity": item.get("stock_quantity", 0),
        "reorder_level": item.get("reorder_level", 5),
        "updated_at": item.get(
            "updated_at",
            datetime.now(timezone.utc)
        )
    }


async def create_inventory(inventory: Inventory):
    existing_item = await inventory_collection.find_one(
        {"product_id": inventory.product_id}
    )

    if existing_item is not None:
        return None

    inventory_data = inventory.model_dump()
    inventory_data["updated_at"] = datetime.now(timezone.utc)

    result = await inventory_collection.insert_one(inventory_data)

    created_item = await inventory_collection.find_one(
        {"_id": result.inserted_id}
    )

    if created_item is None:
        raise RuntimeError("Created item could not be retrieved.")

    return inventory_serializer(created_item)


async def get_all_inventory():
    items = []

    async for item in inventory_collection.find():
        items.append(inventory_serializer(item))

    return items


async def get_inventory_by_product_id(product_id: str):
    item = await inventory_collection.find_one(
        {"product_id": product_id}
    )

    if item is None:
        return None

    return inventory_serializer(item)


async def update_inventory(
    product_id: str,
    inventory: Inventory
):
    existing_item = await inventory_collection.find_one(
        {"product_id": product_id}
    )

    if existing_item is None:
        return None

    updated_data = inventory.model_dump()
    updated_data["updated_at"] = datetime.now(timezone.utc)

    await inventory_collection.update_one(
        {"product_id": product_id},
        {"$set": updated_data}
    )

    updated_item = await inventory_collection.find_one(
        {"product_id": inventory.product_id}
    )

    if updated_item is None:
        raise RuntimeError("Updated item could not be retrieved.")

    return inventory_serializer(updated_item)


async def check_availability(
    product_id: str,
    quantity: int
):
    item = await inventory_collection.find_one(
        {"product_id": product_id}
    )

    if item is None:
        return None

    return item.get("stock_quantity", 0) >= quantity


async def reduce_stock(
    product_id: str,
    quantity: int
):
    if quantity <= 0:
        return False

    item = await inventory_collection.find_one(
        {"product_id": product_id}
    )

    if item is None:
        return None

    current_stock = item.get("stock_quantity", 0)

    if current_stock < quantity:
        return False

    await inventory_collection.update_one(
        {"product_id": product_id},
        {
            "$set": {
                "stock_quantity": current_stock - quantity,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    updated_item = await inventory_collection.find_one(
        {"product_id": product_id}
    )

    if updated_item is None:
        raise RuntimeError("Updated item could not be retrieved.")

    return inventory_serializer(updated_item)


async def delete_inventory(product_id: str):
    result = await inventory_collection.delete_one(
        {"product_id": product_id}
    )

    return result.deleted_count > 0