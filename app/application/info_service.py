from app import __version__
from app.domain.models import ServiceInfo


class InfoService:
    @staticmethod
    def get_service_info() -> ServiceInfo:
        return ServiceInfo(
            message="Hello World", service="wort-wirbel-api", version=__version__
        )
