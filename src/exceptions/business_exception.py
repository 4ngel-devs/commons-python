"""Business logic exceptions for Phoenix microservices."""

from typing import Any, List, Optional

from .base_exception import PhoenixBaseException


class BusinessException(PhoenixBaseException):
    """
    Exception for business logic errors.
    
    Use this for errors related to business rules, domain logic,
    or application-specific errors (e.g., "User not found", "Insufficient balance").
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred
        status_code: HTTP status code (default: 400)
        errors: Optional list of detailed error information
    """

    def __init__(
        self,
        message: str,
        process: str,
        status_code: int = 400,
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize business exception.

        Args:
            message: Error message
            process: Process name where error occurred
            status_code: HTTP status code (default: 400)
            errors: Optional list of detailed errors
        """
        super().__init__(message, process, status_code, errors)

