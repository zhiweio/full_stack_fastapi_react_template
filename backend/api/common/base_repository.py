from typing import Generic, TypeVar, Optional, List, Dict, Any, Tuple, Union
from uuid import UUID
from sqlmodel import SQLModel, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from api.common.utils import get_logger

logger = get_logger(__name__)

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, data: Dict[str, Any]) -> T:
        """创建新记录"""
        try:
            instance = self.model(**data)
            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except Exception:
            await self.session.rollback()
            raise

    async def get_by_id(self, id: UUID) -> Optional[T]:
        """根据ID获取记录"""
        statement = select(self.model).where(self.model.id == id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """获取所有记录"""
        statement = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def update(self, id: UUID, data: Dict[str, Any]) -> Optional[T]:
        """更新记录"""
        try:
            # 先获取现有记录
            statement = select(self.model).where(self.model.id == id)
            result = await self.session.execute(statement)
            existing = result.scalar_one_or_none()

            if not existing:
                return None

            # 更新字段
            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            self.session.add(existing)
            await self.session.commit()
            await self.session.refresh(existing)
            return existing
        except Exception:
            await self.session.rollback()
            raise

    async def delete(self, id: UUID) -> bool:
        """删除记录"""
        try:
            statement = delete(self.model).where(self.model.id == id)
            result = await self.session.execute(statement)
            await self.session.commit()
            return result.rowcount > 0
        except Exception:
            await self.session.rollback()
            raise

    async def count(self, params: Optional[List] = None) -> int:
        """统计记录数量"""
        statement = select(func.count(self.model.id))

        # Apply where conditions if provided
        if params:
            for condition in params:
                statement = statement.where(condition)

        result = await self.session.execute(statement)
        return result.scalar()

    async def find_by(self, **kwargs) -> List[T]:
        """根据条件查找记录"""
        statement = select(self.model)

        for key, value in kwargs.items():
            if hasattr(self.model, key):
                statement = statement.where(getattr(self.model, key) == value)

        result = await self.session.execute(statement)
        return result.scalars().all()

    async def single_or_none(self, **kwargs) -> Optional[T]:
        """根据条件获取单个记录"""
        statement = select(self.model)

        for key, value in kwargs.items():
            if hasattr(self.model, key):
                statement = statement.where(getattr(self.model, key) == value)

        result = await self.session.execute(statement)
        results = result.scalars().all()
        return results[0] if results else None
