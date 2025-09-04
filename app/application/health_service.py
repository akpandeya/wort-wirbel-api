from app.domain.models import HealthStatus


class HealthService:
    @staticmethod
    def get_health_status() -> HealthStatus:
        return HealthStatus(status="healthy", service="wort-wirbel-api")
