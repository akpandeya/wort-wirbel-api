from fastapi import APIRouter

from app.application.services import HealthService, InfoService
from app.domain.models import HealthStatus, ServiceInfo

router = APIRouter()


@router.get("/", response_model=ServiceInfo)
async def hello_world() -> ServiceInfo:
    return InfoService.get_service_info()


@router.get("/health", response_model=HealthStatus)
async def health_check() -> HealthStatus:
    return HealthService.get_health_status()
