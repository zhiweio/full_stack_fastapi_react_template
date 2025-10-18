from uuid import UUID

from api.common.utils import validate_uuid
from api.common.utils import get_logger
from api.core.exceptions import RoleAlreadyExistsException, RoleNotFoundException
from api.domain.dtos.role_dto import (
    CreateRoleDto,
    RoleListDto,
    UpdateRoleDto,
    UpdateRoleDto,
)
from api.domain.entities.role import Role
from api.infrastructure.persistence.repositories.role_repository_impl import (
    RoleRepository,
)

logger = get_logger(__name__)


class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository
        logger.info("Initialized.")

    async def list_roles(self, skip: int = 0, limit: int = 10) -> RoleListDto:
        return await self.role_repository.list(skip=skip, limit=limit)

    async def find_by_name(self, name: str) -> Role:
        """Find a role by its name. Raises RoleNotFoundException if not found."""
        existing = await self.role_repository.single_or_none(name=name)
        if existing is None:
            raise RoleNotFoundException(role_id=name)
        return existing

    async def search_role_by_name(self, name: str) -> list[Role]:
        # Use find_by method from BaseRepository to search for roles by name
        # Since we can't do regex search with SQLModel, we'll get all roles and filter
        all_roles = await self.role_repository.find_by()
        # Filter roles that contain the search name (case insensitive)
        return [role for role in all_roles if name.lower() in role.name.lower()]

    async def get_role_by_id(self, role_id: str) -> Role:
        validated_role_id = validate_uuid(role_id, "Role ID")
        existing = await self.role_repository.get_by_id(id=validated_role_id)
        if existing is None:
            raise RoleNotFoundException(role_id=role_id)
        return existing

    async def create_role(self, role_data: CreateRoleDto) -> UUID:
        existing = await self.role_repository.single_or_none(name=role_data.name)
        if existing is not None:
            raise RoleAlreadyExistsException(name=role_data.name)
        return await self.role_repository.create(data=role_data)

    async def update_role(self, role_id: str, role_data: UpdateRoleDto) -> Role | None:
        validated_role_id = validate_uuid(role_id, "Role ID")
        existing = await self.role_repository.get_by_id(id=validated_role_id)
        if existing is None:
            raise RoleNotFoundException(role_id=role_id)
        return await self.role_repository.update(
            role_id=validated_role_id, data=role_data
        )

    async def delete_role(self, role_id: str) -> None:
        validated_role_id = validate_uuid(role_id, "Role ID")
        if await self.role_repository.delete(id=validated_role_id) is False:
            raise RoleNotFoundException(role_id=role_id)

    async def total_count(self) -> int:
        return await self.role_repository.count()
