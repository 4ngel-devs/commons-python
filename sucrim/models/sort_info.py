"""Sort information model for representing field and direction."""

from pydantic import BaseModel, Field


class SortInfo(BaseModel):
    """
    Information about a sort field and direction.
    
    Represents a single sort field with its direction (asc/desc).
    """

    field: str = Field(description="Field name to sort by")
    direction: str = Field(
        default="asc",
        description="Sort direction: 'asc' or 'desc'"
    )

    class Config:
        """Pydantic configuration."""

        frozen = True

