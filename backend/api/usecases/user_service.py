from typing import Any, Optional
from datetime import datetime

from uuid import UUID

from api.common.utils import get_logger, validate_uuid
from pydantic import EmailStr
from api.common.exceptions import InvalidOperationException
from api.core.exceptions import EmailAlreadyExistsException, UserNotFoundException
from api.domain.dtos.dashboard_dto import TimeSeriesDto
from api.domain.entities.user import User
from api.domain.dtos.user_dto import (
    CreateUserDto,
    UpdateUserDto,
    UserDto,
    UserListDto,
    UserResendActivationEmailRequestDto,
)
from api.domain.entities.user_password_reset import UserPasswordReset
from api.infrastructure.persistence.repositories.user_password_reset_repository_impl import (
    UserPasswordResetRepository,
)
from api.infrastructure.persistence.repositories.user_repository_impl import (
    UserRepository,
)
from api.common.security import hash_it

logger = get_logger(__name__)


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        user_password_reset_repository: UserPasswordResetRepository,
    ):
        self.user_repository = user_repository
        self.user_password_reset_repository = user_password_reset_repository
        logger.info("Initialized.")

    async def list_users(self, skip: int = 0, limit: int = 10) -> UserListDto:
        return await self.user_repository.list(skip=skip, limit=limit)

    async def find_by_email(self, email: EmailStr) -> User:
        """Find user by email. Returns User model. Raises UserNotFoundException if not found."""
        existing = await self.user_repository.single_or_none(email=email)
        if existing is None:
            raise UserNotFoundException(email)
        return existing

    async def get_user_by_id(self, user_id: str) -> User:
        """Get user by ID. Returns User model. Raises UserNotFoundException if not found."""
        user_uuid = validate_uuid(user_id)
        existing = await self.user_repository.get_by_id(id=user_uuid)
        if existing is None:
            raise UserNotFoundException(user_id)
        return existing

    async def create_user(self, user_data: CreateUserDto) -> UUID:
        """Create a new user and returns its ID. Raises EmailAlreadyExistsException if email already exists."""
        existing = await self.user_repository.single_or_none(email=user_data.email)
        if existing is not None:
            raise EmailAlreadyExistsException(user_data.email)
        user_data.password = hash_it(user_data.password)
        user_id = await self.user_repository.create(user_data)

        # Todo: Refactor this to use Celery task to Or fire and forget

        # avoid circular import
        # from api.core.container import get_container

        # auth_service = get_container().get_auth_service()

        # welcome_email = UserResendActivationEmailRequestDto(
        #     email=user_data.email,
        #     first_name=user_data.first_name,
        #     tenant_id=str(user_data.tenant_id),
        #     id=str(user_id)
        # )
        # await auth_service.send_activation_email(welcome_email)
        return user_id

    async def update_user(self, user_id: str, user_data: UpdateUserDto) -> User | None:
        """Update user by ID. Returns updated User model. Raises UserNotFoundException if user does not exist."""
        existing = await self.user_repository.get(id=user_id)
        if existing is None:
            raise UserNotFoundException(user_id)
        return await self.user_repository.update(user_id=user_id, data=user_data)

    async def delete_user(self, user_id: str) -> None:
        """Delete user by ID. Returns None otherwise, Raises UserNotFoundException if user does not exist."""
        if await self.user_repository.delete(id=user_id) is False:
            raise UserNotFoundException(user_id)

    async def update_user_password(
        self, user_id: str, new_password: str
    ) -> User | None:
        """Update user password by ID. Returns updated User model. Raises UserNotFoundException if user does not exist."""
        existing = await self.user_repository.get(id=user_id)
        if existing is None:
            raise UserNotFoundException(user_id)
        hashed_password = hash_it(new_password)
        existing.password = hashed_password
        await self.user_repository.update(existing.id, existing.model_dump())
        return existing

    async def total_count(self, params: Any | None = None) -> int:
        """Get total user count."""
        return await self.user_repository.count(params=params)

    async def request_password_reset(self, email: EmailStr) -> UserPasswordReset:
        """Set password reset for user by ID. Returns None otherwise, Raises InvalidOperationException on failure."""
        try:
            user = await self.find_by_email(email=email)
            return await self.user_password_reset_repository.set_password_reset(
                user_id=str(user.id),
                first_name=user.first_name,
                tenant_id=user.tenant_id,
            )
        except Exception as e:
            logger.error(
                f"Error setting password reset for user with an email: {email} wasn't successful: {e}"
            )
            raise InvalidOperationException(message="Failed to set password reset.")

    async def aggregate(
        self,
        filter_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> list[TimeSeriesDto]:
        """Aggregate users based on filter type and date range. Returns a list of TimeSeriesDto."""
        return await self.user_repository.aggregate(
            filter_type=filter_type, start_date=start_date, end_date=end_date
        )
