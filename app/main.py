"""Applications Management System API - Main Application Entrypoint.

This module initializes the FastAPI application instance, configures CORS,
attaches custom OpenAPI metadata, and mounts the application routers.
"""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.routes.applications import router as applications_router

app = FastAPI(
    title="Applications Management System API",
    description="""
A clean, modular RESTful API system for student and program applications built with **FastAPI** and **Pydantic v2**.

### Architecture Highlights:
- **Separation of Concerns**: Clean layered architecture (Routes -> Schemas/Validation -> Service Layer -> Mock Data).
- **In-Memory Mock Store**: Zero external database dependencies; data initializes with real-world sample applications.
- **Robust Validation**: Schema-level validation for emails, phone numbers, valid URLs, and enum statuses.
- **RESTful Best Practices**: Meaningful HTTP verbs (GET, POST, PUT, PATCH, DELETE) and standardized status codes.

Interactive documentation is available via **Swagger UI** (`/docs`) and **ReDoc** (`/redoc`).
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Enable CORS for frontend integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount application router
app.include_router(applications_router)


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    tags=["Root"],
    summary="API Health and Metadata",
)
def root():
    """Health-check and introductory metadata endpoint."""
    return {
        "system": "Applications Management System API",
        "version": "1.0.0",
        "status": "online",
        "documentation": "/docs",
        "endpoints": {
            "list_applications": "GET /applications",
            "get_application": "GET /applications/{id}",
            "create_application": "POST /applications",
            "update_application": "PUT /applications/{id}",
            "patch_status": "PATCH /applications/{id}/status",
            "delete_application": "DELETE /applications/{id}",
        },
    }
