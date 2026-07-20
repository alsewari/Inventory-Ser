from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Inventory(BaseModel):
    product_id: str = Field(
        ...,
        json_schema_extra={"example": "P1001"}
    )

    product_name: str = Field(
        ...,
        json_schema_extra={"example": "Laptop"}
    )

    stock_quantity: int = Field(
        ...,
        ge=0,
        json_schema_extra={"example": 20}
    )

    reorder_level: int = Field(
        default=5,
        ge=0,
        json_schema_extra={"example": 5}
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )