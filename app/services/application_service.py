"""Application service layer managing CRUD operations and business logic.

This service abstracts data operations over the in-memory mock dataset,
enabling clean separation between API routes and storage logic.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import copy

from app.data.mock_applications import get_initial_mock_applications
from app.schemas.application import (
    ApplicationCreate,
    ApplicationStatus,
    ApplicationUpdate,
)


class ApplicationService:
    """Service class handling student/program application records."""

    def __init__(self) -> None:
        self._applications: List[Dict[str, Any]] = get_initial_mock_applications()

    def reset_dataset(self) -> None:
        """Reset dataset to initial mock seed data."""
        self._applications = get_initial_mock_applications()

    def get_all(
        self,
        status: Optional[str] = None,
        university: Optional[str] = None,
        track: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve all applications, with optional filtering.

        Args:
            status: Filter by status (e.g. 'pending', 'accepted', 'rejected').
            university: Filter by university name (case-insensitive).
            track: Filter by engineering/study track (case-insensitive).

        Returns:
            List of matching application dictionaries.
        """
        results = self._applications

        if status:
            target_status = status.strip().lower()
            results = [
                app for app in results
                if app.get("status") and app["status"].lower() == target_status
            ]

        if university:
            target_uni = university.strip().lower()
            results = [
                app for app in results
                if app.get("university") and target_uni in app["university"].lower()
            ]

        if track:
            target_track = track.strip().lower()
            results = [
                app for app in results
                if app.get("track") and target_track in app["track"].lower()
            ]

        return copy.deepcopy(results)

    def get_by_id(self, application_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve an application by its unique ID.

        Args:
            application_id: The ID of the application.

        Returns:
            Application dictionary if found, None otherwise.
        """
        for app in self._applications:
            if app["id"] == application_id:
                return copy.deepcopy(app)
        return None

    def create(self, payload: ApplicationCreate) -> Dict[str, Any]:
        """Create a new application in the mock dataset.

        Args:
            payload: Validated application creation data.

        Returns:
            Newly created application dictionary with generated ID and timestamp.
        """
        # Generate next ID
        existing_ids = [app["id"] for app in self._applications]
        next_id = (max(existing_ids) + 1) if existing_ids else 1

        # Current UTC timestamp in ISO format
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        new_record: Dict[str, Any] = {
            "id": next_id,
            "full_name": payload.full_name,
            "email": payload.email,
            "phone": payload.phone,
            "university": payload.university,
            "course": payload.course,
            "level": payload.level,
            "track": payload.track,
            "motivation": payload.motivation,
            "portfolio_link": payload.portfolio_link,
            "resume_link": payload.resume_link,
            "join_innovation_club": payload.join_innovation_club,
            "status": payload.status.value if payload.status else ApplicationStatus.PENDING.value,
            "submitted_at": current_time,
        }

        self._applications.append(new_record)
        return copy.deepcopy(new_record)

    def update(self, application_id: int, payload: ApplicationUpdate) -> Optional[Dict[str, Any]]:
        """Update all fields of an existing application.

        Args:
            application_id: The ID of the application to update.
            payload: Validated update payload.

        Returns:
            Updated application dictionary if found, None otherwise.
        """
        for index, app in enumerate(self._applications):
            if app["id"] == application_id:
                # Retain existing ID and submitted_at timestamp
                updated_record = {
                    "id": application_id,
                    "full_name": payload.full_name,
                    "email": payload.email,
                    "phone": payload.phone,
                    "university": payload.university,
                    "course": payload.course,
                    "level": payload.level,
                    "track": payload.track,
                    "motivation": payload.motivation,
                    "portfolio_link": payload.portfolio_link,
                    "resume_link": payload.resume_link,
                    "join_innovation_club": payload.join_innovation_club,
                    "status": payload.status.value if payload.status else app.get("status"),
                    "submitted_at": app.get("submitted_at"),
                }
                self._applications[index] = updated_record
                return copy.deepcopy(updated_record)

        return None

    def update_status(self, application_id: int, new_status: ApplicationStatus) -> Optional[Dict[str, Any]]:
        """Update only the status of an existing application.

        Args:
            application_id: The ID of the application.
            new_status: Validated ApplicationStatus enum.

        Returns:
            Updated application dictionary if found, None otherwise.
        """
        for app in self._applications:
            if app["id"] == application_id:
                app["status"] = new_status.value
                return copy.deepcopy(app)
        return None

    def delete(self, application_id: int) -> bool:
        """Delete an application by its unique ID.

        Args:
            application_id: The ID of the application to delete.

        Returns:
            True if application was deleted, False if not found.
        """
        for index, app in enumerate(self._applications):
            if app["id"] == application_id:
                del self._applications[index]
                return True
        return False


# Singleton service instance
application_service = ApplicationService()
