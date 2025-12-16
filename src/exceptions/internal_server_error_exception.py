"""Internal Server Error (500) exception for Phoenix microservices."""

from typing import Any, List, Optional

from .base_exception import PhoenixBaseException


class InternalServerErrorException(PhoenixBaseException):
    """
    Exception for internal server errors (HTTP 500).
    
    Use this for unexpected server errors that shouldn't occur under normal circumstances.
    
    Args:
        message: Human-readable error message
        process: Process or function where the error occurred (default: "Internal Server Error")
        errors: Optional list of detailed error information
    """

    def __init__(
        self,
        message: str,
        process: str = "Internal Server Error",
        errors: Optional[List[Any]] = None,
    ):
        """
        Initialize internal server error exception.

        Args:
            message: Error message
            process: Process name where error occurred (default: "Internal Server Error")
            errors: Optional list of detailed errors
        """
        super().__init__(message, process, 500, errors)

