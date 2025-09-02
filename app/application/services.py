from app import __version__
from app.domain.models import HealthStatus, ServiceInfo


class InfoService:
    @staticmethod
    def get_service_info() -> ServiceInfo:
        return ServiceInfo(
            message="Hello World", service="wort-wirbel-api", version=__version__
        )


class HealthService:
    @staticmethod
    def get_health_status() -> HealthStatus:
        return HealthStatus(status="healthy", service="wort-wirbel-api")
