"""Pagination data model with sorting support."""

from typing import Optional

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """
    Pagination information for paginated responses.
    
    Supports sorting with sort_by and sort_direction fields.
    """

    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=10, gt=0, description="Page size")
    sort_by: Optional[str] = Field(
        default="created_at",
        description="Column to sort by (default: 'created_at')"
    )
    sort_direction: Optional[str] = Field(
        default="desc",
        description="Sort direction: 'asc' or 'desc' (default: 'desc')"
    )
    total_elements: Optional[int] = Field(
        default=None, ge=0, description="Total number of elements"
    )
    total_pages: Optional[int] = Field(
        default=None, ge=0, description="Total number of pages"
    )

    def model_post_init(self, __context) -> None:
        """Calculate total_pages after total_elements is set."""
        if self.total_elements is not None and self.page_size > 0:
            self.total_pages = (self.total_elements + self.page_size - 1) // self.page_size

    def set_total_elements(self, total: int) -> None:
        """
        Set total elements and automatically calculate total pages.
        
        Args:
            total: Total number of elements
        """
        self.total_elements = total
        if self.page_size > 0:
            self.total_pages = (total + self.page_size - 1) // self.page_size

    class Config:
        """Pydantic configuration."""

        frozen = False  # Allow mutation for setting total_elements

