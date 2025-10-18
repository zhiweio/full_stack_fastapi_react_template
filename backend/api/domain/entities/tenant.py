from datetime import datetime
import re
from typing import Annotated, Literal, Optional, TYPE_CHECKING, List
from urllib.parse import urlparse
from sqlmodel import Field, Relationship
from pydantic import AfterValidator
from api.domain.entities.api_base_model import ApiBaseModel
from api.common.utils import get_host_main_domain_name
from api.core.exceptions import InvalidCustomDomainException, InvalidSubdomainException

if TYPE_CHECKING:
    from .user import User

SUBDOMAIN_REGEX = re.compile(r"^(?!-)[A-Za-z0-9-]{3,63}(?<!-)$")
CUSTOM_DOMAIN_REGEX = re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")


def validate_subdomain(subdomain: str | None) -> str | None:
    """Validate subdomain format. Raises InvalidSubdomainException if invalid. Returns None if subdomain is None."""
    if subdomain is None:
        return None

    main_domain = get_host_main_domain_name()

    if (
        not subdomain.endswith(f".{main_domain}")
        and subdomain != main_domain
        or subdomain == main_domain
    ):
        raise InvalidSubdomainException(subdomain)

    # At this point, it's something like <prefix>.demo.fsrapp.xyz
    label = subdomain.removesuffix(f".{main_domain}")

    # Disallow subdomains that "skip" the main domain (like test.fsrapp.xyz)
    # Example: if main_domain = demo.fsrapp.xyz, then "fsrapp.xyz" would not match ".demo.fsrapp.xyz"
    # so it's already caught above.

    if not SUBDOMAIN_REGEX.match(label):
        raise InvalidSubdomainException(subdomain)

    return subdomain


def validate_custom_domain(domain: str) -> str:
    """
    Validate a custom domain provided by a tenant.

    - Must be a valid domain (e.g., tenant1.com, app.tenant1.com)
    - Cannot be your main domain or a subdomain of it

    :param domain: Domain name provided by the tenant
    :return: The normalized, validated domain name
    :raises InvalidCustomDomainException: if validation fails
    """
    if not domain:
        raise InvalidCustomDomainException("Custom domain is required.")

    # Normalize and strip protocol if mistakenly included
    parsed = urlparse(domain if "://" in domain else f"http://{domain}")
    hostname = parsed.hostname

    if not hostname:
        raise InvalidCustomDomainException("Invalid domain format.")

    if parsed.path not in ("", "/") or parsed.query:
        raise InvalidCustomDomainException(
            "Custom domain must not include paths or query parameters."
        )

    if not CUSTOM_DOMAIN_REGEX.match(hostname):
        raise InvalidCustomDomainException("Invalid domain format.")

    # Ensure it's not your main domain or a subdomain of it
    main_domain = get_host_main_domain_name()  # e.g. "demo.fsrapp.xyz"
    if hostname == main_domain or hostname.endswith(f".{main_domain}"):
        raise InvalidCustomDomainException(
            "Custom domain cannot be your application's main domain or its subdomain."
        )

    return hostname


Subdomain = Annotated[str, AfterValidator(validate_subdomain)]
CustomDomain = Annotated[str, AfterValidator(validate_custom_domain)]


class Tenant(ApiBaseModel, table=True):
    __tablename__ = "tenants"

    name: str = Field(unique=True, index=True, max_length=100)
    subdomain: Optional[Subdomain] = Field(default=None, max_length=255)
    is_active: bool = Field(default=False)
    custom_domain: Optional[CustomDomain] = Field(default=None, max_length=255)
    custom_domain_status: str = Field(default="failed", max_length=50)

    # 关系定义
    users: List["User"] = Relationship(back_populates="tenant")

    def to_serializable_dict(self):
        data = super().to_serializable_dict()
        return {
            **data,
            "name": self.name,
            "subdomain": str(self.subdomain) if self.subdomain else None,
            "is_active": self.is_active,
            "custom_domain": str(self.custom_domain) if self.custom_domain else None,
            "custom_domain_status": str(self.custom_domain_status)
            if self.custom_domain_status
            else None,
        }
