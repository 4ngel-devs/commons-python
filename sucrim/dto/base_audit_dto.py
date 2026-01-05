"""Base DTO with audit fields for tracking creation and updates."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseAuditDto(BaseModel):
    """
    Base DTO with audit fields.
    
    This DTO provides common audit fields that can be extended by other DTOs
    to track who created/updated records and when.
    
    Fields:
        created_by: Username or identifier of who created the record
        created_at: Timestamp when the record was created
        updated_by: Username or identifier of who last updated the record
        updated_at: Timestamp when the record was last updated
    """

    created_by: Optional[str] = Field(
        default=None,
        description="Username or identifier of who created the record"
    )
    created_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the record was created"
    )
    updated_by: Optional[str] = Field(
        default=None,
        description="Username or identifier of who last updated the record"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the record was last updated"
    )

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

