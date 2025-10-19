from celery.utils.functional import first
from sqlalchemy import select, func

from faker import Faker

from api.domain.entities.user import User
from api.domain.entities.role import Role
from api.common.security import hash_it
from api.domain.enum.role import RoleType
from api.common.enums.gender import Gender
from api.common.seeder_utils import get_seed_roles
from api.common.utils import get_logger
from api.infrastructure.persistence.database import db, get_db_session

logger = get_logger(__name__)


async def seed_initial_data():
    """初始化数据的入口函数"""
    logger.info("开始初始化数据...")
    await seed_data()
    logger.info("数据初始化完成")


async def seed_data():
    """初始化角色和用户数据"""
    async for session in get_db_session():
        try:
            # 初始化角色
            await seed_roles(session)

            # 初始化管理员用户
            await seed_admin_user(session)

            # 初始化假用户
            await seed_fake_users(session)

            # 提交事务
            await session.commit()
            logger.info("所有数据初始化完成")

        except Exception as e:
            await session.rollback()
            logger.error(f"数据初始化失败: {e}")
            raise


async def seed_roles(session):
    """初始化角色数据"""
    # 检查是否已存在角色
    result = await session.execute(select(func.count(Role.id)))
    role_count = result.scalar()

    if role_count > 0:
        logger.info("角色数据已存在，跳过初始化")
        return

    # 创建角色
    seed_roles_data = get_seed_roles()

    # 将 Pydantic 模型转换为 SQLAlchemy 实体
    roles = []
    for role_data in seed_roles_data:
        role = Role(
            name=role_data.name,
            description=role_data.description,
            permissions=[perm.value for perm in role_data.permissions],
        )
        roles.append(role)

    session.add_all(roles)
    await session.flush()
    logger.info("角色数据初始化完成")


async def seed_admin_user(session):
    """初始化管理员用户"""
    # 检查管理员用户是否已存在
    result = await session.execute(
        select(User).where(User.email == "admin@example.com")
    )
    existing_admin = result.scalar_one_or_none()

    if existing_admin:
        logger.info("管理员用户已存在，跳过创建")
        return

    # 获取 admin 角色
    result = await session.execute(select(Role).where(Role.name == RoleType.ADMIN))
    admin_role = result.scalar_one_or_none()

    if not admin_role:
        logger.error("admin 角色不存在，无法创建管理员用户")
        return

    # 创建管理员用户
    admin_user = User(
        email="admin@example.com",
        username="admin",
        first_name="Admin",
        last_name="Administrator",
        full_name="Administrator",
        gender=Gender.MALE,
        password=hash_it("Admin@123"),
        is_active=True,
        is_superuser=True,
        role_id=admin_role.id,
    )

    session.add(admin_user)
    await session.flush()
    logger.info("管理员用户创建完成")


async def seed_fake_users(session):
    """初始化假用户数据"""
    # 获取 guest 角色
    result = await session.execute(select(Role).where(Role.name == RoleType.GUEST))
    guest_role = result.scalar_one_or_none()

    if not guest_role:
        logger.error("guest 角色不存在，无法创建访客用户")
        return

    # 检查是否已存在用户（除了管理员）
    result = await session.execute(
        select(func.count(User.id)).where(User.role_id == guest_role.id)
    )
    guest_count = result.scalar()

    if guest_count > 0:
        logger.info("假用户数据已存在，跳过初始化")
        return

    # 创建访客用户
    fake_users = []
    faker = Faker()
    for i in range(3):
        first_name = faker.first_name()
        last_name = faker.last_name()
        full_name = f"{first_name} {last_name}"
        fake_user = User(
            email=faker.email(),
            username=faker.user_name(),
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            gender=faker.random_element(elements=[Gender.MALE, Gender.FEMALE]),
            password=hash_it("Password@123"),
            is_active=True,
            is_superuser=False,
            role_id=guest_role.id,
        )
        fake_users.append(fake_user)

    session.add_all(fake_users)
    await session.flush()
    logger.info(f"创建了 {len(fake_users)} 个访客用户")
