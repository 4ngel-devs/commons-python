"""Base exception class for Phoenix microservices."""

from typing import Any, List, Optional


class PhoenixBaseException(Exception):
    """
    Base exception class for Phoenix microservices.
    
    All custom exceptions should inherit from this class to ensure
    consistent error handling across services.
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred
        status_code: HTTP status code (default: 500)
        errors: Optional list of detailed error information
    """

    def __init__(
        self,
        message: str,
        process: str,
        status_code: int = 500,
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize base exception.

        Args:
            message: Error message
            process: Process name where error occurred
            status_code: HTTP status code
            errors: Optional list of detailed errors
        """
        super().__init__(message)
        self.message = message
        self.process = process
        self.status_code = status_code
        self.errors = errors or []

    def __str__(self) -> str:
        """String representation of the exception."""
        return f"{self.process}: {self.message}"

    def to_dict(self) -> dict:
        """
        Convert exception to dictionary for JSON responses.

        Returns:
            dict: Exception data as dictionary
        """
        return {
            "message": self.message,
            "process": self.process,
            "errors": self.errors,
        }

