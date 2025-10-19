from typing import Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from api.common.base_repository import BaseRepository
from api.common.utils import get_logger, validate_uuid
from api.domain.dtos.role_dto import CreateRoleDto, RoleListDto, UpdateRoleDto
from api.domain.entities.role import Role

logger = get_logger(__name__)


class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(Role, session)

    async def list(
        self, skip: int = 0, limit: int = 10, tenant_id: UUID = None
    ) -> RoleListDto:
        """获取角色列表"""
        # 构建查询条件
        statement = select(Role)
        if tenant_id:
            statement = statement.where(Role.tenant_id == tenant_id)

        # 获取总数
        count_statement = select(func.count(Role.id))
        if tenant_id:
            count_statement = count_statement.where(Role.tenant_id == tenant_id)

        total_result = await self.session.execute(count_statement)
        total = total_result.scalar()

        # 获取分页数据
        statement = statement.offset(skip).limit(limit)
        result = await self.session.execute(statement)
        roles = result.scalars().all()

        return RoleListDto(
            roles=[role.to_serializable_dict() for role in roles],
            skip=skip,
            limit=limit,
            total=total,
            hasPrevious=skip > 0,
            hasNext=skip + limit < total,
        )

    async def create(self, data: CreateRoleDto) -> UUID | None:
        """创建角色"""
        role_data = {
            "name": data.name,
            "description": data.description,
            "tenant_id": data.tenant_id,
        }
        result = await super().create(role_data)
        return result.id if result else None

    async def update(self, role_id: str, data: UpdateRoleDto) -> Optional[Role]:
        """更新角色"""
        try:
            role_uuid = validate_uuid(role_id)
            updated_role = await super().update(
                role_uuid, data.model_dump(exclude_unset=True)
            )
            if updated_role:
                return updated_role
            logger.warning(f"No role found for the given role id: {role_id}")
            return None
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid UUID format for role_id: {role_id}, error: {e}")
            return None

    async def get_by_name(self, name: str, tenant_id: UUID = None) -> Optional[Role]:
        """根据名称获取角色"""
        conditions = {"name": name}
        if tenant_id:
            conditions["tenant_id"] = tenant_id
        return await self.single_or_none(**conditions)
