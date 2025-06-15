from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr, Field


class UserDetail(BaseModel):
    """Model for user details."""

    id: UUID4 = Field(..., description="Unique identifier for the user (UUIDv4)")
    email: EmailStr = Field(..., description="User's email address")
    created_at: datetime = Field(..., description="Account creation timestamp (ISO 8601 format)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "created_at": "2024-06-01T12:34:56Z",
            }
        }
    }
