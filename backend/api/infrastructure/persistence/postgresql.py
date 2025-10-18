from typing import Dict, Optional
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from api.common.utils import get_logger
from api.core.config import settings

logger = get_logger(__name__)


class PostgreSQLDatabase:
    def __init__(self):
        self.engines: Dict[str, AsyncEngine] = {}
        self.session_makers: Dict[str, async_sessionmaker[AsyncSession]] = {}
        self.current_tenant_id: Optional[str] = None
        logger.debug("PostgreSQL Database initializing...")

    def _get_database_url(self, tenant_id: Optional[str] = None) -> str:
        """Generate database URL for tenant or default database"""
        if tenant_id:
            # Multi-tenant database naming: tenant_<tenant_id>
            db_name = f"{settings.tenant_database_prefix}{tenant_id}"
        else:
            # Default database
            db_name = settings.default_database_name

        # Replace database name in the URL
        base_url = settings.database_url
        if base_url.endswith("/"):
            return f"{base_url}{db_name}"
        else:
            # Replace the last part after the last '/' with the new database name
            url_parts = base_url.rsplit("/", 1)
            if len(url_parts) == 2:
                return f"{url_parts[0]}/{db_name}"
            else:
                return f"{base_url}/{db_name}"

    def _get_engine(self, tenant_id: Optional[str] = None) -> AsyncEngine:
        """Get or create engine for tenant or default database"""
        key = tenant_id or "default"

        if key not in self.engines:
            database_url = self._get_database_url(tenant_id)
            logger.debug(f"Creating engine for database: {database_url}")

            self.engines[key] = create_async_engine(
                database_url,
                echo=settings.database_echo,
                poolclass=NullPool,  # Disable connection pooling for multi-tenant
                future=True,
            )

            # Create session maker
            self.session_makers[key] = async_sessionmaker(
                bind=self.engines[key], class_=AsyncSession, expire_on_commit=False
            )

        return self.engines[key]

    async def create_tables(self, tenant_id: Optional[str] = None):
        """Create all tables for the specified tenant or default database"""
        engine = self._get_engine(tenant_id)

        async with engine.begin() as conn:
            # Import all models to ensure they are registered
            from api.domain.entities.user import User
            from api.domain.entities.role import Role
            from api.domain.entities.tenant import Tenant
            from api.domain.entities.ai import ChatSessionAI, ChatHistoryAI
            from api.domain.entities.user_preference import UserPreference
            from api.domain.entities.user_password_reset import UserPasswordReset
            from api.domain.entities.storage_settings import StorageSettings
            from api.domain.entities.user_magic_link import UserMagicLink
            from api.domain.entities.user_passkey import UserPasskey, Challenges

            await conn.run_sync(SQLModel.metadata.create_all)
            logger.info(f"Tables created for database: {tenant_id or 'default'}")

    @asynccontextmanager
    async def get_session(self, tenant_id: Optional[str] = None):
        """Get database session for tenant or default database"""
        key = tenant_id or "default"

        # Ensure engine and session maker exist
        self._get_engine(tenant_id)

        session_maker = self.session_makers[key]
        async with session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def init_db(
        self, tenant_id: Optional[str] = None, create_tables: bool = True
    ):
        """Initialize database for tenant or default"""
        self.current_tenant_id = tenant_id

        if create_tables:
            await self.create_tables(tenant_id)

        if tenant_id:
            logger.debug(f"Database initialized for tenant: {tenant_id}")
        else:
            logger.debug("Default database initialized")

    def set_current_tenant(self, tenant_id: Optional[str]):
        """Set current tenant context"""
        self.current_tenant_id = tenant_id

    def get_current_tenant(self) -> Optional[str]:
        """Get current tenant context"""
        return self.current_tenant_id

    def is_tenant_active(self) -> bool:
        """Check if tenant context is active"""
        return self.current_tenant_id is not None

    async def close(self):
        """Close all database connections"""
        for engine in self.engines.values():
            await engine.dispose()

        self.engines.clear()
        self.session_makers.clear()
        logger.warning("All database connections have been closed.")

    async def drop_database(self, tenant_id: Optional[str] = None):
        """Drop database (for testing purposes)"""
        engine = self._get_engine(tenant_id)

        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            logger.warning(f"Database dropped: {tenant_id or 'default'}")


# Global database instance
postgresql_client = PostgreSQLDatabase()
