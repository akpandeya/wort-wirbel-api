"""
Application services and use cases
"""

from app import __version__
from app.domain.models import HealthStatus, ServiceInfo


class InfoService:
    """Service for providing application information"""

    @staticmethod
    def get_service_info() -> ServiceInfo:
        """Get service information"""
        return ServiceInfo(
            message="Hello World", service="wort-wirbel-api", version=__version__
        )


class HealthService:
    """Service for health checks"""

    @staticmethod
    def get_health_status() -> HealthStatus:
        """Get health status"""
        return HealthStatus(status="healthy", service="wort-wirbel-api")
