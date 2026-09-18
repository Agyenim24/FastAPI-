"""Applications API routes module.

This module defines all RESTful HTTP routes for managing student and program
applications, including filtering, retrieval, creation, full update, status patch,
and deletion.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Path, Query, status

from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
    ApplicationUpdate,
)
from app.services.application_service import application_service

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.get(
    "",
    response_model=List[ApplicationResponse],
    status_code=status.HTTP_200_OK,
    summary="List all applications",
    description="Retrieve all applications from the in-memory store with optional filtering by status, university, and track.",
)
def get_applications(
    status_filter: Optional[str] = Query(
        None,
        alias="status",
        description="Filter applications by status (e.g. 'pending', 'accepted', 'rejected')",
        examples=["pending", "accepted", "rejected"],
    ),
    university_filter: Optional[str] = Query(
        None,
        alias="university",
        description="Filter applications by university name (case-insensitive search, e.g. 'KNUST')",
        examples=["KNUST", "Ashesi University", "UENR"],
    ),
    track_filter: Optional[str] = Query(
        None,
        alias="track",
        description="Filter applications by engineering/study track (case-insensitive search, e.g. 'Backend Engineering')",
        examples=["Backend Engineering", "Radar & RF Systems", "Biomedical Systems"],
    ),
) -> List[Dict[str, Any]]:
    """Get all applications with optional query filters."""
    return application_service.get_all(
        status=status_filter,
        university=university_filter,
        track=track_filter,
    )


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get application by ID",
    description="Retrieve a single application record by its unique identifier.",
    responses={
        404: {
            "description": "Application not found",
            "content": {"application/json": {"example": {"detail": "Application with ID 999 not found"}}},
        }
    },
)
def get_application_by_id(
    application_id: int = Path(
        ...,
        alias="application_id",
        title="Application ID",
        description="The positive integer identifier of the application",
        gt=0,
    ),
) -> Dict[str, Any]:
    """Retrieve an application by ID or raise 404."""
    app = application_service.get_by_id(application_id)
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found",
        )
    return app


@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new application",
    description="Validate and register a new student application in the in-memory dataset.",
    responses={
        201: {"description": "Application successfully created"},
        422: {"description": "Validation error in request payload"},
    },
)
def create_application(payload: ApplicationCreate) -> Dict[str, Any]:
    """Create a new application after full schema validation."""
    return application_service.create(payload)


@router.put(
    "/{application_id}",
    response_model=ApplicationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing application",
    description="Completely update an existing application's details.",
    responses={
        200: {"description": "Application successfully updated"},
        404: {
            "description": "Application not found",
            "content": {"application/json": {"example": {"detail": "Application with ID 999 not found"}}},
        },
        422: {"description": "Validation error in request payload"},
    },
)
def update_application(
    payload: ApplicationUpdate,
    application_id: int = Path(
        ...,
        alias="application_id",
        title="Application ID",
        description="The positive integer identifier of the application",
        gt=0,
    ),
) -> Dict[str, Any]:
    """Perform a full update on an application or raise 404."""
    updated = application_service.update(application_id, payload)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found",
        )
    return updated


@router.patch(
    "/{application_id}/status",
    response_model=ApplicationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update application review status",
    description="Update only the status of an application. Allowed values: 'pending', 'accepted', 'rejected'.",
    responses={
        200: {"description": "Status updated successfully"},
        404: {
            "description": "Application not found",
            "content": {"application/json": {"example": {"detail": "Application with ID 999 not found"}}},
        },
        422: {"description": "Validation error: invalid status value"},
    },
)
def update_application_status(
    payload: ApplicationStatusUpdate,
    application_id: int = Path(
        ...,
        alias="application_id",
        title="Application ID",
        description="The positive integer identifier of the application",
        gt=0,
    ),
) -> Dict[str, Any]:
    """Update application status or raise 404."""
    updated = application_service.update_status(application_id, payload.status)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found",
        )
    return updated


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an application",
    description="Remove an application permanently from the in-memory dataset.",
    responses={
        200: {
            "description": "Application deleted successfully",
            "content": {"application/json": {"example": {"message": "Application 3 successfully deleted", "id": 3}}},
        },
        404: {
            "description": "Application not found",
            "content": {"application/json": {"example": {"detail": "Application with ID 999 not found"}}},
        },
    },
)
def delete_application(
    application_id: int = Path(
        ...,
        alias="application_id",
        title="Application ID",
        description="The positive integer identifier of the application",
        gt=0,
    ),
) -> Dict[str, Any]:
    """Delete an application by ID or raise 404."""
    deleted = application_service.delete(application_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found",
        )
    return {
        "message": f"Application {application_id} successfully deleted",
        "id": application_id,
    }
