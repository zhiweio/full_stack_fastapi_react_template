from typing import Annotated, Optional
from uuid import UUID
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Depends, Request
from api.common.utils import get_host_main_domain_name, get_logger, is_subdomain
from api.core.config import settings

from api.core.container import get_container
from api.infrastructure.persistence.database import db
from api.core.exceptions import TenantNotFoundException
from api.domain.entities.tenant import Tenant

logger = get_logger(__name__)


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id: Optional[str] = None
        tenant_host = get_tenant_host(request)
        logger.debug(f"Tenant host found: {tenant_host}")
        tenant_service = get_container().get_tenant_service()

        if tenant_host:
            try:
                tenant: Tenant
                if is_subdomain(tenant_host):
                    logger.debug(f"Host '{tenant_host}' identified as subdomain.")
                    tenant = await tenant_service.find_by_subdomain(tenant_host)
                else:
                    logger.debug(f"Host '{tenant_host}' identified as custom domain.")
                    tenant = await tenant_service.find_by_custom_domain(tenant_host)

                tenant_id = str(tenant.id)
                logger.debug(
                    f"Tenant ID resolved from custom domain '{tenant_host}': {tenant_id}"
                )
                request.state.frontend_host = tenant_host
            except TenantNotFoundException as e:
                logger.warning(
                    f"Error resolving tenant from custom domain '{tenant_host}': {e}"
                )

        if tenant_id is None:
            tenant_id = (
                request.headers.get("X-Tenant-ID")
                or request.query_params.get("tenant_id")
                or None
            )

        if tenant_id is not None:
            logger.debug(f"Tenant ID found: {tenant_id}")
            try:
                # Convert to UUID and store in request state
                tenant_uuid = UUID(tenant_id)
                request.state.tenant_id = tenant_uuid

                # Initialize database connection for tenant
                await db.init_db(tenant_id=tenant_id)
                logger.debug(f"Database initialized for tenant: {tenant_id}")

                return await call_next(request)
            except ValueError:
                logger.warning(f"Invalid tenant ID format: {tenant_id}")
                request.state.tenant_id = None
                await db.init_db()  # Use default database
        else:
            # No tenant ID provided, use default database
            request.state.tenant_id = None
            await db.init_db()  # Use default database
            logger.debug("No tenant ID provided, using default database.")

        return await call_next(request)


def get_tenant_host(request: Request) -> Optional[str]:
    """
    Extracts the tenant-specific host (subdomain) from the incoming request.
    Returns None if the host matches the main domain.
    """
    # Try HTTP/2 ':authority' → fall back to 'host' → finally use parsed URL
    host = (
        request.headers.get(":authority")
        or request.headers.get("host")
        or request.url.hostname
    )
    if not host:
        return None

    host = host.split(":")[0].lower()  # Remove port if present and convert to lowercase

    # Compare against main domain
    main_domain = get_host_main_domain_name().lower()
    if host == main_domain:
        # If the host is exactly the main domain, return None (no tenant)
        return None

    if host.startswith("localhost") or host.startswith("127.0.0.1"):
        # Handle localhost with optional
        return None

    logger.debug(f"Extracted host: {host}")
    return host


async def get_tenant_id(request: Request) -> UUID | None:
    return getattr(request.state, "tenant_id", None)


async def frontend_dynamic_host(request: Request) -> str:
    return getattr(request.state, "frontend_host", get_host_main_domain_name())


FrontendHost = Annotated[str, Depends(frontend_dynamic_host)]
