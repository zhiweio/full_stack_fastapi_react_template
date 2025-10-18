# MongoDB + Beanie 到 PostgreSQL + SQLModel 迁移指南

## 1. 迁移概述

### 1.1 项目背景
- **当前架构**: MongoDB + Beanie ODM + FastAPI
- **目标架构**: PostgreSQL + SQLModel + SQLAlchemy + FastAPI
- **架构模式**: Clean Architecture (Domain-Infrastructure-Interface)
- **特殊需求**: 多租户支持、依赖注入容器 (Punq)

### 1.2 迁移目标
- 从文档数据库迁移到关系型数据库
- 保持现有的 Clean Architecture 结构
- 维持多租户功能
- 确保数据完整性和一致性
- 最小化业务逻辑层的变更

## 2. 技术栈对比

| 组件 | 当前 (MongoDB) | 目标 (PostgreSQL) |
|------|----------------|-------------------|
| 数据库 | MongoDB | PostgreSQL |
| ORM/ODM | Beanie | SQLModel + SQLAlchemy |
| 主键类型 | PydanticObjectId | UUID |
| 查询语言 | MongoDB Query | SQL |
| 事务支持 | 有限 | 完整的ACID支持 |
| 关系处理 | 嵌入/引用 | 外键约束 |

## 3. 迁移策略

### 3.1 分阶段迁移计划

#### 阶段1: 环境准备 (1-2天)
- [ ] 安装PostgreSQL依赖
- [ ] 更新项目配置
- [ ] 设置开发环境数据库

#### 阶段2: 数据模型重构 (3-5天)
- [ ] 重写实体模型 (Entity层)
- [ ] 创建数据库迁移脚本
- [ ] 更新DTO定义

#### 阶段3: 仓储层重构 (3-4天)
- [ ] 重写BaseRepository
- [ ] 更新所有Repository实现
- [ ] 实现多租户支持

#### 阶段4: 服务层适配 (2-3天)
- [ ] 更新Service层
- [ ] 修复依赖注入
- [ ] 更新中间件

#### 阶段5: 数据迁移 (2-3天)
- [ ] 编写数据迁移脚本
- [ ] 测试数据完整性
- [ ] 性能优化

#### 阶段6: 测试与部署 (2-3天)
- [ ] 单元测试更新
- [ ] 集成测试
- [ ] 生产环境部署

### 3.2 风险评估

| 风险等级 | 风险描述 | 缓解措施 |
|----------|----------|----------|
| 高 | 数据丢失或损坏 | 完整备份、分步迁移、回滚计划 |
| 中 | 性能下降 | 索引优化、查询优化、性能测试 |
| 中 | 多租户功能异常 | 详细测试、渐进式部署 |
| 低 | 依赖冲突 | 版本锁定、虚拟环境隔离 |

## 4. 依赖更新

### 4.1 pyproject.toml 变更

```toml
# 移除的依赖
# "beanie>=2.0.0",
# "motor>=3.7.1", 
# "pymongo>=4.15.1",

# 新增的依赖
dependencies = [
    "sqlmodel>=0.0.14",
    "sqlalchemy>=2.0.23",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",
    "psycopg2-binary>=2.9.9",
    # ... 其他现有依赖保持不变
]
```

### 4.2 配置文件更新

```python
# api/core/config.py
class Settings(BaseSettings):
    # 移除 MongoDB 配置
    # mongo_uri: str = "mongodb://localhost:27017"
    # mongo_db_name: str = "myapp"
    
    # 新增 PostgreSQL 配置
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/myapp"
    database_echo: bool = False  # SQL日志输出
    
    # 多租户数据库配置
    tenant_database_prefix: str = "tenant_"
    default_database_name: str = "myapp"
    
    # 其他配置保持不变...
```

## 5. 数据模型重构

### 5.1 基础模型重构

#### 当前 ApiBaseModel (Beanie)
```python
# api/domain/entities/api_base_model.py
from beanie import Document, PydanticObjectId

class ApiBaseModel(Document):
    created_at: datetime = get_utc_now()
    updated_at: datetime = get_utc_now()
    tenant_id: Optional[PydanticObjectId] = None
```

#### 新的 ApiBaseModel (SQLModel)
```python
# api/domain/entities/api_base_model.py
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class ApiBaseModel(SQLModel):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    tenant_id: Optional[UUID] = Field(default=None, foreign_key="tenants.id")
    
    class Config:
        from_attributes = True
```

### 5.2 用户模型重构

#### 当前 User 模型 (Beanie)
```python
from beanie import Indexed, PydanticObjectId
from api.domain.entities.api_base_model import ApiBaseModel

class User(ApiBaseModel):
    first_name: str
    last_name: str
    email: EmailStr = Indexed(EmailStr, unique=True)
    gender: Gender = Indexed(str)
    role_id: Optional[PydanticObjectId] = None
    is_active: bool
    activated_at: Optional[datetime] = None
    image_url: Optional[str] = None
    password: str
    
    class Settings:
        name = "users"
```

#### 新的 User 模型 (SQLModel)
```python
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Boolean, DateTime, Index
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .role import Role
    from .tenant import Tenant

class User(ApiBaseModel, table=True):
    __tablename__ = "users"
    
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: str = Field(unique=True, index=True, max_length=255)
    gender: str = Field(max_length=20, index=True)
    role_id: Optional[UUID] = Field(default=None, foreign_key="roles.id")
    is_active: bool = Field(default=False)
    activated_at: Optional[datetime] = Field(default=None)
    image_url: Optional[str] = Field(default=None, max_length=500)
    password: str = Field(max_length=255)
    
    # 关系定义
    role: Optional["Role"] = Relationship(back_populates="users")
    tenant: Optional["Tenant"] = Relationship(back_populates="users")
    
    # 索引定义
    __table_args__ = (
        Index('idx_user_email_tenant', 'email', 'tenant_id', unique=True),
        Index('idx_user_gender', 'gender'),
        Index('idx_user_active', 'is_active'),
    )
```

## 6. 数据库连接重构

### 6.1 数据库连接管理

```python
# api/infrastructure/persistence/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel
from typing import AsyncGenerator
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
            pool_recycle=300
        )
        
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        self.current_tenant_id = tenant_id
        logger.info(f"Database initialized for tenant: {tenant_id or 'default'}")
        
    def _get_tenant_database_url(self, tenant_id: str) -> str:
        """构建租户专用数据库URL"""
        base_url = settings.database_url
        # 替换数据库名称为租户专用名称
        tenant_db_name = f"{settings.tenant_database_prefix}{tenant_id}"
        return base_url.replace(settings.default_database_name, tenant_db_name)
        
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
```

### 6.2 多租户中间件更新

```python
# api/interfaces/middlewares/tenant_middleware.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from api.infrastructure.persistence.database import db
from api.core.config import settings

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id = None
        
        # 从请求头获取租户ID
        if settings.multi_tenancy_strategy == "header":
            tenant_id = request.headers.get("X-Tenant-ID")
        elif settings.multi_tenancy_strategy == "subdomain":
            host = request.headers.get("host", "")
            if "." in host:
                subdomain = host.split(".")[0]
                if subdomain != settings.host_main_domain_prefix:
                    tenant_id = subdomain
                    
        # 初始化对应的数据库连接
        try:
            await db.init_db(tenant_id=tenant_id)
            request.state.tenant_id = tenant_id
            
            response = await call_next(request)
            return response
            
        except Exception as e:
            logger.error(f"Tenant middleware error: {e}")
            raise HTTPException(status_code=500, detail="Database connection failed")
```

## 7. 仓储层重构

### 7.1 基础仓储重构

#### 当前 BaseRepository (Beanie)
```python
from beanie import Document, PydanticObjectId

class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model
```

#### 新的 BaseRepository (SQLModel)
```python
# api/common/base_repository.py
from typing import TypeVar, Generic, Optional, List, Dict, Any
from sqlmodel import SQLModel, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from uuid import UUID
from api.infrastructure.persistence.database import db

T = TypeVar("T", bound=SQLModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model
        
    async def get_session(self) -> AsyncSession:
        """获取数据库会话"""
        async for session in db.get_session():
            return session
            
    async def create(self, data: Dict[str, Any]) -> T:
        """创建新记录"""
        session = await self.get_session()
        try:
            instance = self.model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance
        except Exception:
            await session.rollback()
            raise
            
    async def get_by_id(self, id: UUID) -> Optional[T]:
        """根据ID获取记录"""
        session = await self.get_session()
        statement = select(self.model).where(self.model.id == id)
        result = await session.exec(statement)
        return result.first()
        
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """获取所有记录"""
        session = await self.get_session()
        statement = select(self.model).offset(skip).limit(limit)
        result = await session.exec(statement)
        return result.all()
        
    async def update(self, id: UUID, data: Dict[str, Any]) -> Optional[T]:
        """更新记录"""
        session = await self.get_session()
        try:
            statement = (
                update(self.model)
                .where(self.model.id == id)
                .values(**data)
                .returning(self.model)
            )
            result = await session.exec(statement)
            updated_instance = result.first()
            if updated_instance:
                await session.commit()
                await session.refresh(updated_instance)
            return updated_instance
        except Exception:
            await session.rollback()
            raise
            
    async def delete(self, id: UUID) -> bool:
        """删除记录"""
        session = await self.get_session()
        try:
            statement = delete(self.model).where(self.model.id == id)
            result = await session.exec(statement)
            await session.commit()
            return result.rowcount > 0
        except Exception:
            await session.rollback()
            raise
            
    async def count(self) -> int:
        """统计记录数量"""
        session = await self.get_session()
        statement = select(func.count(self.model.id))
        result = await session.exec(statement)
        return result.first()
        
    async def find_by(self, **kwargs) -> List[T]:
        """根据条件查找记录"""
        session = await self.get_session()
        statement = select(self.model)
        
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                statement = statement.where(getattr(self.model, key) == value)
                
        result = await session.exec(statement)
        return result.all()
        
    async def single_or_none(self, **kwargs) -> Optional[T]:
        """根据条件获取单个记录"""
        results = await self.find_by(**kwargs)
        return results[0] if results else None
```

### 7.2 用户仓储重构

```python
# api/infrastructure/persistence/repositories/user_repository_impl.py
from typing import Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy import and_
from api.common.base_repository import BaseRepository
from api.domain.entities.user import User
from api.domain.dtos.user_dto import CreateUserDto, UpdateUserDto, UserListDto
from api.common.utils import get_logger

logger = get_logger(__name__)

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
        
    async def list(self, skip: int = 0, limit: int = 10, tenant_id: UUID = None) -> UserListDto:
        """获取用户列表"""
        session = await self.get_session()
        
        # 构建查询条件
        statement = select(User)
        if tenant_id:
            statement = statement.where(User.tenant_id == tenant_id)
            
        # 获取总数
        count_statement = select(func.count(User.id))
        if tenant_id:
            count_statement = count_statement.where(User.tenant_id == tenant_id)
            
        total_result = await session.exec(count_statement)
        total = total_result.first()
        
        # 获取分页数据
        statement = statement.offset(skip).limit(limit)
        result = await session.exec(statement)
        users = result.all()
        
        return UserListDto(
            users=[user.model_dump() for user in users],
            skip=skip,
            limit=limit,
            total=total,
            hasPrevious=skip > 0,
            hasNext=skip + limit < total
        )
        
    async def create(self, data: CreateUserDto) -> UUID:
        """创建用户"""
        user_data = data.model_dump()
        user = await super().create(user_data)
        return user.id
        
    async def get_by_email(self, email: str, tenant_id: UUID = None) -> Optional[User]:
        """根据邮箱获取用户"""
        session = await self.get_session()
        statement = select(User).where(User.email == email)
        
        if tenant_id:
            statement = statement.where(User.tenant_id == tenant_id)
            
        result = await session.exec(statement)
        return result.first()
        
    async def update(self, user_id: UUID, data: UpdateUserDto) -> Optional[User]:
        """更新用户"""
        update_data = data.model_dump(exclude_unset=True)
        return await super().update(user_id, update_data)
```

## 8. 数据迁移策略

### 8.1 迁移脚本结构

```python
# scripts/migrate_data.py
import asyncio
import asyncpg
from motor.motor_asyncio import AsyncIOMotorClient
from api.core.config import settings
from api.common.utils import get_logger

logger = get_logger(__name__)

class DataMigrator:
    def __init__(self):
        self.mongo_client = None
        self.pg_pool = None
        
    async def init_connections(self):
        """初始化数据库连接"""
        # MongoDB连接
        self.mongo_client = AsyncIOMotorClient(settings.mongo_uri)
        self.mongo_db = self.mongo_client[settings.mongo_db_name]
        
        # PostgreSQL连接
        self.pg_pool = await asyncpg.create_pool(settings.database_url)
        
    async def migrate_users(self):
        """迁移用户数据"""
        logger.info("开始迁移用户数据...")
        
        # 从MongoDB获取用户数据
        users_cursor = self.mongo_db.users.find({})
        
        async for user_doc in users_cursor:
            try:
                # 数据转换
                user_data = {
                    'id': str(uuid4()),  # 生成新的UUID
                    'first_name': user_doc.get('first_name'),
                    'last_name': user_doc.get('last_name'),
                    'email': user_doc.get('email'),
                    'gender': user_doc.get('gender'),
                    'is_active': user_doc.get('is_active', False),
                    'password': user_doc.get('password'),
                    'created_at': user_doc.get('created_at'),
                    'updated_at': user_doc.get('updated_at'),
                    'tenant_id': str(user_doc.get('tenant_id')) if user_doc.get('tenant_id') else None
                }
                
                # 插入PostgreSQL
                async with self.pg_pool.acquire() as conn:
                    await conn.execute("""
                        INSERT INTO users (id, first_name, last_name, email, gender, 
                                         is_active, password, created_at, updated_at, tenant_id)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    """, *user_data.values())
                    
                logger.info(f"迁移用户: {user_data['email']}")
                
            except Exception as e:
                logger.error(f"迁移用户失败 {user_doc.get('email')}: {e}")
                
    async def migrate_all(self):
        """执行完整迁移"""
        await self.init_connections()
        
        try:
            await self.migrate_users()
            # 添加其他实体的迁移...
            
        finally:
            if self.mongo_client:
                self.mongo_client.close()
            if self.pg_pool:
                await self.pg_pool.close()

# 运行迁移
async def main():
    migrator = DataMigrator()
    await migrator.migrate_all()

if __name__ == "__main__":
    asyncio.run(main())
```

### 8.2 Alembic 迁移配置

```python
# alembic/env.py
from sqlmodel import SQLModel
from api.domain.entities import *  # 导入所有实体
from api.core.config import settings

# Alembic配置
target_metadata = SQLModel.metadata

def run_migrations_online():
    """在线模式运行迁移"""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.database_url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

## 9. 测试策略

### 9.1 单元测试更新

```python
# tests/conftest.py
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import SQLModel
from api.infrastructure.persistence.database import db

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    """测试数据库引擎"""
    engine = create_async_engine(
        "postgresql+asyncpg://test:test@localhost:5432/test_db",
        echo=True
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        
    await engine.dispose()

@pytest.fixture
async def session(test_engine):
    """测试会话"""
    async with AsyncSession(test_engine) as session:
        yield session
        await session.rollback()
```

### 9.2 仓储测试示例

```python
# tests/repositories/test_user_repository.py
import pytest
from uuid import uuid4
from api.infrastructure.persistence.repositories.user_repository_impl import UserRepository
from api.domain.entities.user import User
from api.domain.dtos.user_dto import CreateUserDto

@pytest.mark.asyncio
async def test_create_user(session):
    """测试创建用户"""
    repo = UserRepository()
    
    user_data = CreateUserDto(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        gender="male",
        password="hashed_password",
        is_active=True
    )
    
    user_id = await repo.create(user_data)
    assert user_id is not None
    
    # 验证用户已创建
    user = await repo.get_by_id(user_id)
    assert user is not None
    assert user.email == "test@example.com"
```

## 10. 性能优化

### 10.1 数据库索引策略

```sql
-- 用户表索引
CREATE INDEX CONCURRENTLY idx_users_email_tenant ON users(email, tenant_id);
CREATE INDEX CONCURRENTLY idx_users_active ON users(is_active) WHERE is_active = true;
CREATE INDEX CONCURRENTLY idx_users_created_at ON users(created_at DESC);

-- 角色表索引
CREATE INDEX CONCURRENTLY idx_roles_name_tenant ON roles(name, tenant_id);

-- 复合索引用于常见查询
CREATE INDEX CONCURRENTLY idx_users_tenant_active ON users(tenant_id, is_active) 
WHERE is_active = true;
```

### 10.2 连接池配置

```python
# 生产环境数据库配置
DATABASE_CONFIG = {
    "pool_size": 20,
    "max_overflow": 30,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "echo": False
}
```

## 11. 部署和回滚计划

### 11.1 部署步骤

1. **准备阶段**
   - 备份MongoDB数据
   - 准备PostgreSQL环境
   - 部署新版本到测试环境

2. **迁移阶段**
   - 停止应用服务
   - 执行数据迁移脚本
   - 启动新版本应用

3. **验证阶段**
   - 功能测试
   - 性能测试
   - 数据完整性检查

### 11.2 回滚计划

```bash
#!/bin/bash
# rollback.sh - 回滚脚本

echo "开始回滚到MongoDB版本..."

# 1. 停止当前服务
docker-compose down

# 2. 恢复代码版本
git checkout mongodb-version

# 3. 恢复MongoDB数据
mongorestore --uri="mongodb://localhost:27017/myapp" ./backup/

# 4. 启动MongoDB版本服务
docker-compose -f docker-compose.mongodb.yml up -d

echo "回滚完成"
```

## 12. 监控和维护

### 12.1 监控指标

- 数据库连接池使用率
- 查询执行时间
- 事务成功/失败率
- 多租户数据库性能

### 12.2 日志配置

```python
# 数据库操作日志
import logging

# SQLAlchemy日志配置
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
```

## 13. 总结

这个迁移计划提供了从MongoDB + Beanie到PostgreSQL + SQLModel的完整路径。关键成功因素包括:

1. **充分的测试**: 确保所有功能在新架构下正常工作
2. **数据完整性**: 验证迁移后的数据准确性
3. **性能优化**: 合理的索引和查询优化
4. **回滚准备**: 完整的回滚计划以应对意外情况
5. **渐进式部署**: 分阶段部署降低风险

预计整个迁移过程需要2-3周时间，建议在低峰期执行关键的数据迁移步骤。