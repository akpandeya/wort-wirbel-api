"""
Domain models for the wort-wirbel application
"""

from pydantic import BaseModel


class ServiceInfo(BaseModel):
    """Service information model"""

    message: str
    service: str
    version: str


class HealthStatus(BaseModel):
    """Health status model"""

    status: str
    service: str
