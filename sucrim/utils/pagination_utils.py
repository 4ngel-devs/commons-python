"""Utilities for working with pagination objects."""

from typing import Tuple

from sucrim.models.pagination import Pagination
from sucrim.utils.sort_utils import SortUtils


class PaginationUtils:
    """Utility class for pagination operations."""

    @staticmethod
    def create_pageable_params(pagination: Pagination) -> Tuple[int, int]:
        """
        Create pageable parameters (page, size) from Pagination object.

        Converts 1-indexed page to 0-indexed for database queries.

        Args:
            pagination: Pagination object

        Returns:
            Tuple of (page_index, page_size) where page_index is 0-indexed
        """
        # Convert 1-indexed page to 0-indexed
        page_index = max(0, pagination.page - 1)
        return (page_index, pagination.page_size)

    @staticmethod
    def create_pageable_with_sort(pagination: Pagination) -> Tuple[int, int, list]:
        """
        Create pageable parameters with sort information.

        Returns page index (0-indexed), page size, and list of SortInfo objects.

        Args:
            pagination: Pagination object with sort_by and sort_direction

        Returns:
            Tuple of (page_index, page_size, sort_infos)
        """
        page_index, page_size = PaginationUtils.create_pageable_params(pagination)
        sort_infos = SortUtils.create_sort(
            pagination.sort_by, pagination.sort_direction
        )
        return (page_index, page_size, sort_infos)

    @staticmethod
    def create_pageable_dict(pagination: Pagination) -> dict:
        """
        Create a dictionary with pageable parameters.

        Useful for ORM queries that accept dictionaries.

        Args:
            pagination: Pagination object

        Returns:
            Dictionary with 'page', 'size', and 'sort' keys
        """
        page_index, page_size = PaginationUtils.create_pageable_params(pagination)
        sort_infos = SortUtils.create_sort(
            pagination.sort_by, pagination.sort_direction
        )

        return {
            "page": page_index,
            "size": page_size,
            "sort": SortUtils.to_sort_dict(sort_infos),
        }

