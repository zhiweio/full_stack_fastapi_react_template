from typing import Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from api.common.base_repository import BaseRepository
from api.common.exceptions import ConflictException
from api.common.utils import get_logger
from api.domain.dtos.tenant_dto import CreateTenantDto, TenantListDto
from api.domain.entities.tenant import Tenant
from api.infrastructure.persistence.database import db

logger = get_logger(__name__)


class TenantRepository(BaseRepository[Tenant]):
    def __init__(self):
        super().__init__(Tenant)

    async def list(self, skip: int = 0, limit: int = 10) -> TenantListDto:
        """获取租户列表"""
        async with db.get_session() as session:
            # 获取总数
            count_statement = select(func.count(Tenant.id))
            total_result = await session.execute(count_statement)
            total = total_result.scalar()

            # 获取分页数据
            statement = select(Tenant).offset(skip).limit(limit)
            result = await session.execute(statement)
            tenants = result.scalars().all()

            tenant_dto = [tenant.to_serializable_dict() for tenant in tenants]
            return TenantListDto(
                tenants=tenant_dto,
                skip=skip,
                limit=limit,
                total=total,
                hasPrevious=skip > 0,
                hasNext=skip + limit < total,
            )

    async def create(self, data: CreateTenantDto) -> UUID | None:
        """创建租户"""
        try:
            tenant_data = {"name": data.name, "subdomain": data.subdomain}
            result = await super().create(tenant_data)
            return result.id if result else None
        except IntegrityError as ex:
            logger.error(f"Error creating tenant: {str(ex)}")
            raise ConflictException("Tenant", data.name)

    async def get_by_subdomain(self, subdomain: str) -> Optional[Tenant]:
        """根据子域名获取租户"""
        return await self.single_or_none(subdomain=subdomain)

    async def get_by_custom_domain(self, custom_domain: str) -> Optional[Tenant]:
        """根据自定义域名获取租户"""
        return await self.single_or_none(custom_domain=custom_domain)
