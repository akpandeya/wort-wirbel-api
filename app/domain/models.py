from pydantic import BaseModel


class ServiceInfo(BaseModel):
    message: str
    service: str
    version: str


class HealthStatus(BaseModel):
    status: str
    service: str
