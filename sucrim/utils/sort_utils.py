"""Utilities for parsing and creating sort objects."""

from typing import List, Optional

from sucrim.models.sort_info import SortInfo


class SortUtils:
    """Utility class for parsing and creating sort objects."""

    ASC = "asc"
    DESC = "desc"

    @staticmethod
    def parse_sort(sort_string: Optional[str]) -> List[SortInfo]:
        """
        Parse a sort string into a list of SortInfo objects.

        Supports formats:
        - "field:direction,field2:direction2" (e.g., "name:asc,createdAt:desc")
        - "field" (defaults to asc)
        - Multiple fields separated by commas

        Examples:
            >>> SortUtils.parse_sort("name:asc,createdAt:desc")
            [SortInfo(field='name', direction='asc'), SortInfo(field='createdAt', direction='desc')]
            >>> SortUtils.parse_sort("name")
            [SortInfo(field='name', direction='asc')]
            >>> SortUtils.parse_sort(None)
            []

        Args:
            sort_string: The sort string to parse (e.g., "name:asc,createdAt:desc")

        Returns:
            List of SortInfo objects
        """
        if not sort_string or not sort_string.strip():
            return []

        sort_infos: List[SortInfo] = []
        parts = sort_string.split(",")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            if ":" in part:
                # Format: "field:direction"
                field_direction = part.split(":", 1)
                if len(field_direction) == 2:
                    field = field_direction[0].strip()
                    direction = field_direction[1].strip().lower()
                    # Validate direction
                    if direction not in (SortUtils.ASC, SortUtils.DESC):
                        direction = SortUtils.ASC
                    sort_infos.append(SortInfo(field=field, direction=direction))
            else:
                # Format: "field" - default to asc
                sort_infos.append(SortInfo(field=part, direction=SortUtils.ASC))

        return sort_infos

    @staticmethod
    def create_sort(
        sort_by: Optional[str],
        default_direction: Optional[str] = None,
    ) -> List[SortInfo]:
        """
        Create a list of SortInfo from a sort_by string and optional default direction.

        If sort_by contains commas or colons, it's treated as a complex sort
        and parsed accordingly. Otherwise, it's treated as a simple field
        with the default_direction (or 'asc' if not provided).

        Examples:
            >>> SortUtils.create_sort("name:asc,createdAt:desc")
            [SortInfo(field='name', direction='asc'), SortInfo(field='createdAt', direction='desc')]
            >>> SortUtils.create_sort("name", "desc")
            [SortInfo(field='name', direction='desc')]
            >>> SortUtils.create_sort(None)
            []

        Args:
            sort_by: The field(s) to sort by
            default_direction: Default direction if sort_by doesn't contain direction (default: 'asc')

        Returns:
            List of SortInfo objects
        """
        if not sort_by or not sort_by.strip():
            return []

        # Check if it's a complex sort (multiple fields or with explicit directions)
        if "," in sort_by or ":" in sort_by:
            return SortUtils.parse_sort(sort_by)

        # Simple sort with default direction
        direction = (
            default_direction.lower()
            if default_direction
            and default_direction.lower() in (SortUtils.ASC, SortUtils.DESC)
            else SortUtils.ASC
        )
        return [SortInfo(field=sort_by.strip(), direction=direction)]

    @staticmethod
    def to_sort_dict(sort_infos: List[SortInfo]) -> List[dict]:
        """
        Convert a list of SortInfo to a list of dictionaries.

        Useful for ORM queries that accept sort dictionaries.

        Args:
            sort_infos: List of SortInfo objects

        Returns:
            List of dictionaries with 'field' and 'direction' keys
        """
        return [
            {"field": info.field, "direction": info.direction}
            for info in sort_infos
        ]

