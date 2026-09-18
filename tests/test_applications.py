"""Comprehensive test suite for Applications Management System REST API.

Tests cover all CRUD operations, filtering parameters, schema validation,
HTTP status codes, and error conditions using FastAPI's TestClient.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.application_service import application_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_in_memory_data():
    """Reset the mock dataset before each test to guarantee test isolation."""
    application_service.reset_dataset()
    yield
    application_service.reset_dataset()


# ==============================================================================
# 1. Root and Health Endpoint Tests
# ==============================================================================

def test_root_endpoint():
    """Verify that GET / returns API metadata and online status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "version" in data
    assert "documentation" in data


# ==============================================================================
# 2. GET /applications Tests
# ==============================================================================

def test_get_all_applications():
    """Verify retrieval of all initial mock applications."""
    response = client.get("/applications")
    assert response.status_code == 200
    applications = response.json()
    assert len(applications) == 4

    ids = [app["id"] for app in applications]
    assert ids == [2, 3, 4, 5]

    # Verify Application 2 preserves nulls
    app2 = next(a for a in applications if a["id"] == 2)
    assert app2["full_name"] == "Ama Serwaa Owusu"
    assert app2["university"] is None
    assert app2["course"] is None


def test_get_application_by_id_success():
    """Verify retrieval of an existing application by ID."""
    response = client.get("/applications/3")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["full_name"] == "Yaw Mensah"
    assert data["email"] == "yawmensah@gmail.com"
    assert data["university"] == "KNUST"
    assert data["course"] == "Electrical Engineering"
    assert data["track"] == "Radar & RF Systems"
    assert data["status"] == "pending"


def test_get_nonexistent_application():
    """Verify that requesting a non-existent application ID returns 404."""
    response = client.get("/applications/999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


# ==============================================================================
# 3. POST /applications (Creation & Validation Tests)
# ==============================================================================

def test_create_valid_application():
    """Verify successful creation of a new application with 201 Created."""
    payload = {
        "full_name": "Kofi Mensah",
        "email": "kofi.mensah@example.com",
        "phone": "0241234567",
        "university": "University of Ghana",
        "course": "Computer Science",
        "level": "3rd Year",
        "track": "Backend Engineering",
        "motivation": "Eager to learn FastAPI and API design.",
        "portfolio_link": "https://github.com/kofimensah",
        "resume_link": "https://linkedin.com/in/kofimensah",
        "join_innovation_club": True,
        "status": "pending",
    }
    response = client.post("/applications", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 6
    assert data["full_name"] == "Kofi Mensah"
    assert data["email"] == "kofi.mensah@example.com"
    assert data["status"] == "pending"
    assert data["submitted_at"] is not None

    # Verify record is now in GET /applications
    get_res = client.get("/applications/6")
    assert get_res.status_code == 200
    assert get_res.json()["full_name"] == "Kofi Mensah"


def test_create_invalid_application_empty_name():
    """Verify validation failure for empty or whitespace-only name."""
    payload = {
        "full_name": "   ",
        "email": "valid.email@example.com",
        "phone": "0241234567",
    }
    response = client.post("/applications", json=payload)
    assert response.status_code == 422


def test_create_invalid_application_invalid_email():
    """Verify validation failure for invalid email address format."""
    payload = {
        "full_name": "Jane Doe",
        "email": "not-an-email",
        "phone": "0241234567",
    }
    response = client.post("/applications", json=payload)
    assert response.status_code == 422


def test_create_invalid_application_invalid_phone():
    """Verify validation failure for phone number with too few digits."""
    payload = {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "123",
    }
    response = client.post("/applications", json=payload)
    assert response.status_code == 422


def test_create_invalid_application_invalid_url():
    """Verify validation failure for malformed portfolio URL."""
    payload = {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "0241234567",
        "portfolio_link": "not-a-valid-url",
    }
    response = client.post("/applications", json=payload)
    assert response.status_code == 422


def test_create_invalid_application_missing_required_field():
    """Verify validation failure when required field (e.g. phone) is missing."""
    payload = {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
    }
    response = client.post("/applications", json=payload)
    assert response.status_code == 422


# ==============================================================================
# 4. PUT /applications/{id} Tests
# ==============================================================================

def test_update_application_success():
    """Verify full update of an existing application."""
    payload = {
        "full_name": "Yaw Mensah Updated",
        "email": "yawmensah.new@gmail.com",
        "phone": "0558876999",
        "university": "KNUST",
        "course": "Telecommunications Engineering",
        "level": "Completed",
        "track": "Satellite Communications",
        "motivation": "Updated research direction.",
        "portfolio_link": "https://github.com/yawmensah-updated",
        "resume_link": "https://linkedin.com/in/yawmensah-updated",
        "join_innovation_club": True,
        "status": "accepted",
    }
    response = client.put("/applications/3", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["full_name"] == "Yaw Mensah Updated"
    assert data["course"] == "Telecommunications Engineering"
    assert data["status"] == "accepted"


def test_update_nonexistent_application():
    """Verify that updating a non-existent application returns 404."""
    payload = {
        "full_name": "Ghost User",
        "email": "ghost@example.com",
        "phone": "0241234567",
    }
    response = client.put("/applications/999", json=payload)
    assert response.status_code == 404


# ==============================================================================
# 5. PATCH /applications/{id}/status Tests
# ==============================================================================

def test_update_application_status_success():
    """Verify patching an application's status to accepted."""
    response = client.patch("/applications/3/status", json={"status": "accepted"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["status"] == "accepted"

    # Verify status changed when fetching record again
    get_res = client.get("/applications/3")
    assert get_res.json()["status"] == "accepted"


def test_reject_invalid_status():
    """Verify that setting an unsupported status returns 422."""
    response = client.patch("/applications/3/status", json={"status": "waitlisted"})
    assert response.status_code == 422


def test_patch_status_nonexistent_application():
    """Verify patching status on a non-existent application returns 404."""
    response = client.patch("/applications/999/status", json={"status": "accepted"})
    assert response.status_code == 404


# ==============================================================================
# 6. DELETE /applications/{id} Tests
# ==============================================================================

def test_delete_application_success():
    """Verify deleting an existing application returns 200 and removes it."""
    response = client.delete("/applications/3")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert "deleted" in data["message"].lower()

    # Confirm application no longer exists
    get_res = client.get("/applications/3")
    assert get_res.status_code == 404


def test_delete_nonexistent_application():
    """Verify deleting a non-existent application returns 404."""
    response = client.delete("/applications/999")
    assert response.status_code == 404


# ==============================================================================
# 7. Query Filtering Tests
# ==============================================================================

def test_filter_applications_by_status():
    """Verify GET /applications?status=pending filters correctly."""
    response = client.get("/applications?status=pending")
    assert response.status_code == 200
    apps = response.json()
    assert len(apps) == 1
    assert apps[0]["id"] == 3
    assert apps[0]["status"] == "pending"


def test_filter_applications_by_university():
    """Verify GET /applications?university=KNUST returns matching applicants."""
    response = client.get("/applications?university=KNUST")
    assert response.status_code == 200
    apps = response.json()
    assert len(apps) == 1
    assert apps[0]["full_name"] == "Yaw Mensah"
    assert apps[0]["university"] == "KNUST"


def test_filter_applications_by_track():
    """Verify GET /applications?track=Backend%20Engineering returns matching applicants."""
    response = client.get("/applications?track=Backend%20Engineering")
    assert response.status_code == 200
    apps = response.json()
    assert len(apps) == 1
    assert apps[0]["full_name"] == "Priscilla Adjei"
    assert apps[0]["track"] == "Backend Engineering"


def test_filter_applications_no_match():
    """Verify empty list is returned when filter criteria matches nothing."""
    response = client.get("/applications?university=NonExistentUniversity")
    assert response.status_code == 200
    apps = response.json()
    assert apps == []
