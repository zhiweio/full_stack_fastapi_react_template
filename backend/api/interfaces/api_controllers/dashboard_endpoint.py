from typing import Literal

from fastapi import Depends, Query, APIRouter
from api.common.utils import get_date_range
from api.core.dependencies import UserServiceDep
from api.domain.dtos.dashboard_dto import DashboardMetricsDto
from api.infrastructure.security.current_user import CurrentUser
from api.usecases.user_service import UserService


router = APIRouter(prefix="/dashboard")  # type: ignore
router.tags = ["Dashboard"]


@router.get("/", response_model=DashboardMetricsDto)
async def get_dashboard_metrics(
    user_service: UserServiceDep,
    current_user: CurrentUser,
    filter: Literal["today", "this_week", "last_3_months", "all"] = Query("all"),
):
    # Simulate fetching data based on the filter
    start_date, end_date, group_format = get_date_range(filter)

    # 构建查询条件
    match_stage = []
    if start_date:
        from api.domain.entities.user import User

        # 将带时区的datetime转换为naive datetime以匹配数据库字段类型
        start_naive = (
            start_date.replace(tzinfo=None) if start_date.tzinfo else start_date
        )
        end_naive = end_date.replace(tzinfo=None) if end_date.tzinfo else end_date

        match_stage = [User.created_at >= start_naive, User.created_at <= end_naive]

    # 获取时间序列数据
    timeseries = await user_service.aggregate(
        filter_type=filter, start_date=start_date, end_date=end_date
    )

    # 获取总用户数
    total_users = await user_service.total_count()

    # 计算加入的用户数
    if match_stage:
        joined_users = await user_service.total_count(params=match_stage)
    else:
        joined_users = total_users

    data = {
        "filter": filter,
        "joined_users": joined_users,
        "total_users": total_users,
        "timeseries": timeseries,
    }
    return DashboardMetricsDto(**data)
