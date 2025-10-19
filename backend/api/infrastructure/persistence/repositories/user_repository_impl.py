from typing import Optional, Any, List, Dict
from uuid import UUID
from sqlmodel import select
from sqlalchemy import func, text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from api.common.utils import get_logger, validate_uuid, get_utc_now
from api.domain.dtos.user_dto import CreateUserDto, UpdateUserDto, UserListDto
from api.domain.dtos.dashboard_dto import TimeSeriesDto
from api.domain.entities.user import User
from api.common.base_repository import BaseRepository

logger = get_logger(__name__)


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def list(
        self, skip: int = 0, limit: int = 10, tenant_id: UUID = None
    ) -> UserListDto:
        """获取用户列表"""
        # 构建查询条件
        statement = select(User)
        if tenant_id:
            statement = statement.where(User.tenant_id == tenant_id)

        # 获取总数
        count_statement = select(func.count(User.id))
        if tenant_id:
            count_statement = count_statement.where(User.tenant_id == tenant_id)

        total_result = await self.session.execute(count_statement)
        total = total_result.scalar()

        # 获取分页数据
        statement = statement.offset(skip).limit(limit)
        result = await self.session.execute(statement)
        users = result.scalars().all()

        return UserListDto(
            users=[user.to_serializable_dict() for user in users],
            skip=skip,
            limit=limit,
            total=total,
            hasPrevious=skip > 0,
            hasNext=skip + limit < total,
        )

    async def create(self, data: CreateUserDto) -> UUID | None:
        """创建用户"""
        user_data = {
            "email": data.email,
            "first_name": data.first_name,
            "last_name": data.last_name,
            "gender": data.gender,
            "password": data.password,
            "is_active": False,
            "role_id": data.role_id,
            "tenant_id": data.tenant_id,
        }
        result = await super().create(user_data)
        return result.id if result else None

    async def update(self, user_id: UUID, data: UpdateUserDto) -> Optional[User]:
        """更新用户"""
        validated_user_id = validate_uuid(str(user_id), "User ID")
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        return await super().update(validated_user_id, update_data)

    async def aggregate(
        self,
        filter_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[TimeSeriesDto]:
        """进行聚合查询，用于仪表板时间序列数据"""
        from sqlalchemy import func, extract

        try:
            # 根据过滤类型确定分组方式
            if filter_type == "today":
                # 按小时分组
                time_group = func.to_char(
                    func.date_trunc("hour", User.created_at), "HH24:MI"
                )
            elif filter_type == "this_week":
                # 按天分组
                time_group = func.to_char(
                    func.date_trunc("day", User.created_at), "YYYY-MM-DD"
                )
            elif filter_type == "last_3_months":
                # 按月分组
                time_group = func.to_char(
                    func.date_trunc("month", User.created_at), "YYYY-MM"
                )
            else:
                # 默认按天分组
                time_group = func.to_char(
                    func.date_trunc("day", User.created_at), "YYYY-MM-DD"
                )

            # 构建基础查询
            query = select(
                time_group.label("time_or_date"), func.count(User.id).label("count")
            ).select_from(User)

            # 添加时间范围过滤
            if start_date:
                # 将带时区的datetime转换为naive datetime以匹配数据库字段类型
                start_naive = (
                    start_date.replace(tzinfo=None) if start_date.tzinfo else start_date
                )
                query = query.where(User.created_at >= start_naive)
            if end_date:
                # 将带时区的datetime转换为naive datetime以匹配数据库字段类型
                end_naive = (
                    end_date.replace(tzinfo=None) if end_date.tzinfo else end_date
                )
                query = query.where(User.created_at <= end_naive)

            # 分组和排序
            query = query.group_by(time_group).order_by(time_group)

            # 执行查询
            result = await self.session.execute(query)
            rows = result.fetchall()

            # 转换为 TimeSeriesDto
            return [
                TimeSeriesDto(time_or_date=row.time_or_date, count=row.count)
                for row in rows
            ]

        except Exception as e:
            logger.error(f"Error in aggregate query: {e}")
            return []

    async def get_by_email(self, email: str, tenant_id: UUID = None) -> Optional[User]:
        """根据邮箱获取用户"""
        conditions = {"email": email}
        if tenant_id:
            conditions["tenant_id"] = tenant_id
        return await self.single_or_none(**conditions)

    async def activate_user(self, user_id: UUID) -> Optional[User]:
        """激活用户"""
        from datetime import datetime

        return await self.update(
            user_id, {"is_active": True, "activated_at": get_utc_now()}
        )
