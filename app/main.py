"""
Main FastAPI application module
"""

from fastapi import FastAPI

from app import __version__

app = FastAPI(
    title="Wort-Wirbel API",
    description="API for the Wort-Wirbel application",
    version=__version__,
)


@app.get("/")
async def hello_world():
    """
    Hello World endpoint

    Returns:
        dict: A simple greeting message
    """
    return {
        "message": "Hello World",
        "service": "wort-wirbel-api",
        "version": __version__,
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring

    Returns:
        dict: Health status
    """
    return {"status": "healthy", "service": "wort-wirbel-api"}
