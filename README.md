# Applications Management System REST API

A production-grade, layered REST API backend for managing student and program applications, built with **FastAPI**, **Pydantic v2**, and an **in-memory mock dataset**.

This project demonstrates clean software architecture, RESTful API design principles, strict schema validation, CRUD operations, query parameter filtering, and automated testing without requiring a persistent database engine.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture & Design Pattern](#architecture--design-pattern)
- [Project Structure](#project-structure)
- [Features](#features)
- [Mock Dataset](#mock-dataset)
- [Installation & Setup](#installation--setup)
- [Running the Development Server](#running-the-development-server)
- [Interactive API Documentation](#interactive-api-documentation)
- [API Endpoints Reference](#api-endpoints-reference)
  - [Root / Health Check](#root--health-check)
  - [List Applications (with Filtering)](#list-applications)
  - [Get Application by ID](#get-application-by-id)
  - [Create Application](#create-application)
  - [Update Application (Full)](#update-application)
  - [Update Application Status (Partial)](#update-application-status)
  - [Delete Application](#delete-application)
- [Data Validation Rules](#data-validation-rules)
- [HTTP Status Codes Reference](#http-status-codes-reference)
- [Automated Testing](#automated-testing)
- [In-Memory Storage & Limitations](#in-memory-storage--limitations)
- [Future Database Integration](#future-database-integration)

---

## Project Overview

The **Applications Management System** manages admissions and enrollment applications for technical tracks (such as Backend Engineering, Radar & RF Systems, and Biomedical Systems).

The application is structured to follow **Separation of Concerns (SoC)** and **Single Responsibility Principle (SRP)**, decoupling route handlers from domain validation and storage logic.

---

## Architecture & Design Pattern

The application follows a 4-tier layered architecture:

```
+-------------------------------------------------------------+
|                      Client / Browser                       |
|           (HTTP Requests / REST Clients / Swagger UI)        |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
|                     API Routes Layer                        |
|                  (app/routes/applications.py)               |
|      - HTTP verb routing (GET, POST, PUT, PATCH, DELETE)    |
|      - Query parameter & path parameter extraction          |
|      - HTTP status code mapping                             |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
|                 Schemas / Validation Layer                  |
|                 (app/schemas/application.py)                |
|      - Pydantic v2 Data Models                              |
|      - Field validators (Email regex, Phone, URLs, Enums)   |
|      - Strict JSON schema serialization                     |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
|                    Service Domain Layer                     |
|                (app/services/application_service.py)        |
|      - Business & CRUD logic                                |
|      - Query filtering (status, university, track)          |
|      - ID generation & submission timestamps                |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
|                   Mock Data Store Layer                     |
|                  (app/data/mock_applications.py)            |
|      - In-memory collection of applications                 |
|      - Factory function for reproducible seed data          |
+-------------------------------------------------------------+
```

### Request Lifecycle Example (`GET /applications/3`)
1. **Client** issues `GET /applications/3`.
2. **FastAPI Router** captures `application_id=3` and validates that it is a positive integer (`gt=0`).
3. **Application Service** queries the in-memory data store for an application with `id == 3`.
4. **Mock Store** returns the dictionary for Yaw Mensah.
5. **Pydantic Schema** serializes the dictionary into an `ApplicationResponse` model.
6. **Router** returns JSON with status `200 OK`.

---

## Project Structure

```
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entrypoint, CORS, OpenAPI metadata
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── applications.py      # HTTP route definitions & controller logic
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── application.py       # Pydantic v2 schemas, validation, and status enums
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── application_service.py # In-memory CRUD, filtering, business rules
│   │
│   └── data/
│       ├── __init__.py
│       └── mock_applications.py # Initial seed data (Applications 2, 3, 4, 5)
│
├── tests/
│   ├── __init__.py
│   └── test_applications.py     # 21 comprehensive pytest unit & integration tests
│
├── requirements.txt             # Project dependencies
├── README.md                    # System documentation
└── .gitignore                   # Ignored files (virtual environments, caches)
```

---

## Features

- **Standard RESTful Endpoints**: Full CRUD capabilities (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
- **Query Parameter Filtering**: Filter applications by `status`, `university`, and `track`.
- **Strict Data Validation**:
  - Email format validation.
  - Phone number validation (digits count, Ghana/international patterns).
  - Valid HTTP/HTTPS protocol validation for URLs.
  - Allowed status enum validation (`pending`, `accepted`, `rejected`).
  - Required vs. optional fields handling.
- **Automated Interactive Docs**: Fully typed OpenAPI 3.1 documentation via Swagger UI (`/docs`) and ReDoc (`/redoc`).
- **Comprehensive Test Suite**: Automated tests using `pytest` and `fastapi.testclient.TestClient`.
- **Zero Database Setup**: Plug-and-play in-memory mock dataset.

---

## Mock Dataset

The service starts pre-populated with the following mock applications:

| ID | Full Name | University | Track | Status | Notes |
|:---|:---|:---|:---|:---|:---|
| **2** | Ama Serwaa Owusu | *None* | *None* | *None* | Missing optional fields preserved as `null` |
| **3** | Yaw Mensah | KNUST | Radar & RF Systems | `pending` | Join Innovation Club: `true` |
| **4** | Priscilla Adjei | Ashesi University | Backend Engineering | `accepted` | Join Innovation Club: `true` |
| **5** | Daniel Kofi Asante | UENR | Biomedical Systems | `rejected` | Join Innovation Club: `false` |

---

## Installation & Setup

### Prerequisites
- Python 3.10 or newer (tested on Python 3.14)
- `pip` package manager

### 1. Clone or Navigate to Directory
```powershell
cd d:\backend
```

### 2. (Optional) Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

---

## Running the Development Server

Start the Uvicorn ASGI server with hot reloading enabled:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Once running, the API is available at:
- **Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
- **Alternative ReDoc UI**: `http://127.0.0.1:8000/redoc`
- **OpenAPI Schema (JSON)**: `http://127.0.0.1:8000/openapi.json`

---

## Interactive API Documentation

FastAPI automatically inspects Pydantic models, route decorators, and type hints to generate an interactive documentation portal:

1. Open `http://127.0.0.1:8000/docs` in your browser.
2. Click on any route (e.g. `POST /applications` or `PATCH /applications/{id}/status`).
3. Click **"Try it out"** to submit test payloads and inspect live responses directly.

---

## API Endpoints Reference

### Root / Health Check

- **URL**: `/`
- **Method**: `GET`
- **Purpose**: Verify API status and inspect available endpoints.
- **Parameters**: None
- **Response**: `200 OK`

```json
{
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
    "delete_application": "DELETE /applications/{id}"
  }
}
```

---

### List Applications

- **URL**: `/applications`
- **Method**: `GET`
- **Purpose**: Retrieve all applications with optional query filtering.
- **Query Parameters**:
  - `status` (*optional*, string): `pending`, `accepted`, `rejected`
  - `university` (*optional*, string): Case-insensitive filter (e.g., `KNUST`)
  - `track` (*optional*, string): Case-insensitive filter (e.g., `Backend Engineering`)
- **Status Codes**:
  - `200 OK`: Successful retrieval

#### Example Request:
```bash
curl -X GET "http://127.0.0.1:8000/applications?university=KNUST"
```

#### Example Response (`200 OK`):
```json
[
  {
    "id": 3,
    "full_name": "Yaw Mensah",
    "email": "yawmensah@gmail.com",
    "phone": "0558876123",
    "university": "KNUST",
    "course": "Electrical Engineering",
    "level": "4th Year",
    "track": "Radar & RF Systems",
    "motivation": "To improve my knowledge in RF systems, radar engineering, and wireless communications.",
    "portfolio_link": "https://github.com/yawmensah",
    "resume_link": "https://linkedin.com/in/yawmensah",
    "join_innovation_club": true,
    "status": "pending",
    "submitted_at": "2026-05-05T08:45:30Z"
  }
]
```

---

### Get Application by ID

- **URL**: `/applications/{id}`
- **Method**: `GET`
- **Purpose**: Fetch a single application by its numeric identifier.
- **Path Parameters**:
  - `id` (*required*, integer, `> 0`): Application ID
- **Status Codes**:
  - `200 OK`: Found
  - `404 Not Found`: Application ID does not exist

#### Example Request:
```bash
curl -X GET "http://127.0.0.1:8000/applications/4"
```

#### Example Response (`200 OK`):
```json
{
  "id": 4,
  "full_name": "Priscilla Adjei",
  "email": "priscilla.adjei@gmail.com",
  "phone": "0203344556",
  "university": "Ashesi University",
  "course": "Software Engineering",
  "level": "3rd Year",
  "track": "Backend Engineering",
  "motivation": "I want to strengthen my backend engineering skills using FastAPI and modern software architecture.",
  "portfolio_link": "https://github.com/priscillaadjei",
  "resume_link": "https://linkedin.com/in/priscillaadjei",
  "join_innovation_club": true,
  "status": "accepted",
  "submitted_at": "2026-05-06T14:18:22Z"
}
```

#### Error Response (`404 Not Found`):
```json
{
  "detail": "Application with ID 999 not found"
}
```

---

### Create Application

- **URL**: `/applications`
- **Method**: `POST`
- **Purpose**: Validate and persist a new application in the mock dataset.
- **Request Body** (`application/json`):
  - `full_name` (*required*, string): Minimum 2 characters
  - `email` (*required*, string): Valid email address
  - `phone` (*required*, string): Valid phone number (min 7 digits)
  - `university` (*optional*, string)
  - `course` (*optional*, string)
  - `level` (*optional*, string)
  - `track` (*optional*, string)
  - `motivation` (*optional*, string)
  - `portfolio_link` (*optional*, string): Valid HTTP/HTTPS URL
  - `resume_link` (*optional*, string): Valid HTTP/HTTPS URL
  - `join_innovation_club` (*optional*, boolean)
  - `status` (*optional*, string): Defaults to `pending`
- **Status Codes**:
  - `201 Created`: Application successfully registered
  - `422 Unprocessable Entity`: Validation failure

#### Example Request:
```bash
curl -X POST "http://127.0.0.1:8000/applications" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Abena Osei",
    "email": "abena.osei@gmail.com",
    "phone": "0249876543",
    "university": "University of Ghana",
    "course": "Computer Engineering",
    "level": "3rd Year",
    "track": "Backend Engineering",
    "motivation": "Passionate about building scalable distributed systems and REST APIs.",
    "portfolio_link": "https://github.com/abenaosei",
    "resume_link": "https://linkedin.com/in/abenaosei",
    "join_innovation_club": true
  }'
```

#### Example Response (`201 Created`):
```json
{
  "id": 6,
  "full_name": "Abena Osei",
  "email": "abena.osei@gmail.com",
  "phone": "0249876543",
  "university": "University of Ghana",
  "course": "Computer Engineering",
  "level": "3rd Year",
  "track": "Backend Engineering",
  "motivation": "Passionate about building scalable distributed systems and REST APIs.",
  "portfolio_link": "https://github.com/abenaosei",
  "resume_link": "https://linkedin.com/in/abenaosei",
  "join_innovation_club": true,
  "status": "pending",
  "submitted_at": "2026-09-18T20:00:00Z"
}
```

---

### Update Application

- **URL**: `/applications/{id}`
- **Method**: `PUT`
- **Purpose**: Full update of an existing application record.
- **Path Parameters**: `id` (integer)
- **Status Codes**:
  - `200 OK`: Updated successfully
  - `404 Not Found`: ID does not exist
  - `422 Unprocessable Entity`: Validation error

#### Example Request:
```bash
curl -X PUT "http://127.0.0.1:8000/applications/3" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Yaw Mensah",
    "email": "yawmensah@gmail.com",
    "phone": "0558876123",
    "university": "KNUST",
    "course": "Electrical & Electronic Engineering",
    "level": "Final Year",
    "track": "Radar & RF Systems",
    "motivation": "Deepening practical experience in radar hardware and software integration.",
    "portfolio_link": "https://github.com/yawmensah",
    "resume_link": "https://linkedin.com/in/yawmensah",
    "join_innovation_club": true,
    "status": "accepted"
  }'
```

---

### Update Application Status

- **URL**: `/applications/{id}/status`
- **Method**: `PATCH`
- **Purpose**: Modify only the application's review status.
- **Path Parameters**: `id` (integer)
- **Request Body**:
  ```json
  {
    "status": "accepted"
  }
  ```
  *(Allowed values: `pending`, `accepted`, `rejected`)*
- **Status Codes**:
  - `200 OK`: Status updated
  - `404 Not Found`: Application ID not found
  - `422 Unprocessable Entity`: Invalid status value

#### Example Request:
```bash
curl -X PATCH "http://127.0.0.1:8000/applications/3/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "accepted"}'
```

#### Example Response (`200 OK`):
```json
{
  "id": 3,
  "full_name": "Yaw Mensah",
  "email": "yawmensah@gmail.com",
  "phone": "0558876123",
  "university": "KNUST",
  "course": "Electrical Engineering",
  "level": "4th Year",
  "track": "Radar & RF Systems",
  "motivation": "To improve my knowledge in RF systems, radar engineering, and wireless communications.",
  "portfolio_link": "https://github.com/yawmensah",
  "resume_link": "https://linkedin.com/in/yawmensah",
  "join_innovation_club": true,
  "status": "accepted",
  "submitted_at": "2026-05-05T08:45:30Z"
}
```

---

### Delete Application

- **URL**: `/applications/{id}`
- **Method**: `DELETE`
- **Purpose**: Remove an application record from memory.
- **Path Parameters**: `id` (integer)
- **Status Codes**:
  - `200 OK`: Successfully deleted
  - `404 Not Found`: Application ID not found

#### Example Request:
```bash
curl -X DELETE "http://127.0.0.1:8000/applications/5"
```

#### Example Response (`200 OK`):
```json
{
  "message": "Application 5 successfully deleted",
  "id": 5
}
```

---

## Data Validation Rules

| Field | Rule | Error Behavior |
|:---|:---|:---|
| `full_name` | String, minimum 2 non-whitespace characters | Returns `422` if empty, whitespace, or `< 2` chars |
| `email` | Valid email pattern (`user@domain.tld`) | Returns `422` if regex pattern fails |
| `phone` | String, at least 7 digits, digits/symbols allowed | Returns `422` if invalid format or insufficient digits |
| `portfolio_link` | Optional, must be valid HTTP/HTTPS URL | Returns `422` if malformed URL |
| `resume_link` | Optional, must be valid HTTP/HTTPS URL | Returns `422` if malformed URL |
| `status` | Enum: `pending`, `accepted`, `rejected` | Returns `422` if unlisted value |
| `join_innovation_club` | Boolean (`true`, `false`) or `null` | Returns `422` if not boolean |
| `id` | Positive integer (`> 0`) | Returns `422` if string or non-positive |

---

## HTTP Status Codes Reference

- **`200 OK`**: Successful `GET`, `PUT`, `PATCH`, or `DELETE` requests.
- **`201 Created`**: Successful `POST /applications` creation.
- **`400 Bad Request`**: Malformed request syntax or unprocessable parameters.
- **`404 Not Found`**: Target application ID does not exist in the dataset.
- **`422 Unprocessable Entity`**: Payload failed Pydantic validation rules.
- **`500 Internal Server Error`**: Unexpected server exception.

---

## Automated Testing

The project includes an automated test suite with **21 test cases** written in `pytest`.

### Test Coverage Breakdown:
- Root health-check endpoint (`GET /`)
- Full application listing (`GET /applications`)
- Field preservation for incomplete mock records (Application 2)
- Query filtering by `status`, `university`, and `track`
- Fetch by ID (`GET /applications/{id}`)
- 404 response on non-existent records
- Valid creation (`POST /applications`) with ID and timestamp assignment
- Rejection of invalid payloads (empty name, bad email, bad phone, bad URL, missing required fields)
- Full update (`PUT /applications/{id}`)
- Status patch (`PATCH /applications/{id}/status`)
- Rejection of invalid status enums
- Successful deletion (`DELETE /applications/{id}`) and post-deletion 404 verification

### Running the Test Suite:
```powershell
python -m pytest backend/tests/test_applications.py -v
```

---

## In-Memory Storage & Limitations

> [!WARNING]
> **Runtime In-Memory Persistence Only**
>
> All application data created, modified, or deleted during server execution is stored in Python memory (`list` in `app/services/application_service.py`).
>
> - When the FastAPI server or process restarts, **all runtime changes will be reset** to the initial seed dataset (Applications 2, 3, 4, and 5).
> - This mock setup is ideal for local development, unit testing, frontend prototyping, and API architecture learning.

---

## Future Database Integration

To transition this project from an in-memory mock store to a persistent database (such as **PostgreSQL**, **MySQL**, or **SQLite**), the layered architecture enables seamless adaptation with zero changes to route handlers:

1. **Add ORM / Driver**:
   Install `sqlalchemy` and `alembic` (and `psycopg2-binary` for PostgreSQL):
   ```bash
   pip install sqlalchemy alembic psycopg2-binary
   ```
2. **Define Database Models**:
   Create an `app/models/application.py` file with SQLAlchemy `declarative_base()`:
   ```python
   class ApplicationModel(Base):
       __tablename__ = "applications"
       id = Column(Integer, primary_key=True, index=True)
       full_name = Column(String(150), nullable=False)
       email = Column(String(255), nullable=False, index=True)
       phone = Column(String(50), nullable=False)
       university = Column(String(150), nullable=True)
       course = Column(String(150), nullable=True)
       level = Column(String(50), nullable=True)
       track = Column(String(100), nullable=True)
       motivation = Column(Text, nullable=True)
       portfolio_link = Column(String(500), nullable=True)
       resume_link = Column(String(500), nullable=True)
       join_innovation_club = Column(Boolean, nullable=True)
       status = Column(String(20), default="pending")
       submitted_at = Column(DateTime, default=datetime.utcnow)
   ```
3. **Refactor Service Layer**:
   Update `app/services/application_service.py` to inject `db: Session = Depends(get_db)` and perform queries (`db.query(ApplicationModel)...`) instead of list comprehensions.
4. **Preserve Schemas and Routes**:
   The existing `app/schemas/application.py` models already configure `from_attributes = True`, meaning they will automatically serialize SQLAlchemy ORM objects into JSON without modifying route signatures.
