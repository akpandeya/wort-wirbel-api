from fastapi import FastAPI

from app import __version__
from app.presentation.api import router

app = FastAPI(
    title="Wort-Wirbel API",
    description="API for the Wort-Wirbel application",
    version=__version__,
)

app.include_router(router)
