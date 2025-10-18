from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager
from api.core.config import settings
from api.common.utils import get_logger

logger = get_logger(__name__)


class Database:
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.current_tenant_id: Optional[str] = None

    async def init_db(self, database_url: str = None, tenant_id: str = None):
        """初始化数据库连接"""
        if database_url is None:
            if tenant_id:
                # 多租户数据库
                database_url = self._get_tenant_database_url(tenant_id)
            else:
                # 默认数据库
                database_url = settings.database_url

        self.engine = create_async_engine(
            database_url,
            echo=settings.database_echo,
            pool_pre_ping=True,
            pool_recycle=300,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

        self.current_tenant_id = tenant_id
        logger.info(f"Database initialized for tenant: {tenant_id or 'default'}")

    def _get_tenant_database_url(self, tenant_id: str) -> str:
        """构建租户专用数据库URL"""
        base_url = settings.database_url
        # 替换数据库名称为租户专用名称
        tenant_db_name = f"{settings.tenant_database_prefix}{tenant_id}"
        return base_url.replace(settings.default_database_name, tenant_db_name)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取数据库会话"""
        if not self.session_factory:
            raise RuntimeError("Database not initialized")

        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def create_tables(self):
        """创建数据库表"""
        if not self.engine:
            raise RuntimeError("Database not initialized")

        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def close(self):
        """关闭数据库连接"""
        if self.engine:
            await self.engine.dispose()


# 全局数据库实例
db = Database()


# 依赖注入函数
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话的依赖注入函数"""
    async with db.get_session() as session:
        yield session
