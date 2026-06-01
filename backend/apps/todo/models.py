from typing import Optional
import uuid
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class TaskModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "My important task",
                "completed": True,
            }
        },
    )

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str = Field(...)
    completed: bool = False


class UpdateTaskModel(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "My important task",
                "completed": True,
            }
        }
    )

    name: Optional[str] = None
    completed: Optional[bool] = None
