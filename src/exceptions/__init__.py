"""Exception classes for Phoenix microservices."""

from .bad_request_exception import BadRequestException
from .base_exception import PhoenixBaseException
from .business_exception import BusinessException
from .conflict_exception import ConflictException
from .forbidden_exception import ForbiddenException
from .internal_server_error_exception import InternalServerErrorException
from .not_found_exception import NotFoundException
from .service_unavailable_exception import ServiceUnavailableException
from .unauthorized_exception import UnauthorizedException
from .unprocessable_entity_exception import UnprocessableEntityException
from .validation_exception import ValidationException

__all__ = [
    "PhoenixBaseException",
    "BusinessException",
    "ValidationException",
    "BadRequestException",
    "UnauthorizedException",
    "ForbiddenException",
    "NotFoundException",
    "ConflictException",
    "UnprocessableEntityException",
    "InternalServerErrorException",
    "ServiceUnavailableException",
]
