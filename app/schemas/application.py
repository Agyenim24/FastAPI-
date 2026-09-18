"""Application schemas and validation models.

This module defines Pydantic models for request validation, data serialization,
and status enums used across the Applications Management System.
"""

from enum import Enum
import re
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ApplicationStatus(str, Enum):
    """Allowed application statuses."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
URL_REGEX = re.compile(r"^https?://[a-zA-Z0-9-._~:/?#\[\]@!$&'()*+,;=%]+$")
PHONE_REGEX = re.compile(r"^\+?[0-9\s\-()]{7,20}$")


class ApplicationBase(BaseModel):
    """Base schema with common validation rules."""
    full_name: str = Field(..., description="Full legal name of applicant", min_length=2, max_length=150)
    email: str = Field(..., description="Valid applicant email address")
    phone: str = Field(..., description="Phone or WhatsApp number")
    university: Optional[str] = Field(None, description="Current or attended university", max_length=150)
    course: Optional[str] = Field(None, description="Course / degree of study", max_length=150)
    level: Optional[str] = Field(None, description="Academic level or year", max_length=50)
    track: Optional[str] = Field(None, description="Applied engineering or study track", max_length=100)
    motivation: Optional[str] = Field(None, description="Statement of motivation or interest", max_length=2000)
    portfolio_link: Optional[str] = Field(None, description="Portfolio or GitHub profile URL")
    resume_link: Optional[str] = Field(None, description="Resume or LinkedIn profile URL")
    join_innovation_club: Optional[bool] = Field(None, description="Interest in joining the Innovation Club")

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Full name cannot be empty or whitespace only.")
        if len(trimmed) < 2:
            raise ValueError("Full name must be at least 2 characters long.")
        return trimmed

    @field_validator("email")
    @classmethod
    def validate_email_address(cls, v: str) -> str:
        trimmed = v.strip()
        if not EMAIL_REGEX.match(trimmed):
            raise ValueError("Invalid email address format.")
        return trimmed.lower()

    @field_validator("phone")
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        trimmed = v.strip()
        if not PHONE_REGEX.match(trimmed):
            raise ValueError("Invalid phone number format.")
        # Ensure at least 7 digits
        digits_only = re.sub(r"\D", "", trimmed)
        if len(digits_only) < 7:
            raise ValueError("Phone number must contain at least 7 digits.")
        return trimmed

    @field_validator("portfolio_link", "resume_link")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        trimmed = v.strip()
        if not trimmed:
            return None
        if not URL_REGEX.match(trimmed):
            raise ValueError("Invalid URL format. Must be a valid HTTP or HTTPS URL.")
        return trimmed


class ApplicationCreate(ApplicationBase):
    """Schema for creating a new application."""
    status: Optional[ApplicationStatus] = Field(
        default=ApplicationStatus.PENDING,
        description="Initial status of the application",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "Kofi Mensah",
                "email": "kofi.mensah@example.com",
                "phone": "0240001122",
                "university": "University of Ghana",
                "course": "Computer Science",
                "level": "3rd Year",
                "track": "Backend Engineering",
                "motivation": "Eager to master REST APIs, microservices, and backend architecture.",
                "portfolio_link": "https://github.com/kofimensah",
                "resume_link": "https://linkedin.com/in/kofimensah",
                "join_innovation_club": True,
                "status": "pending",
            }
        }
    )


class ApplicationUpdate(ApplicationBase):
    """Schema for full update of an existing application."""
    status: Optional[ApplicationStatus] = Field(
        None,
        description="Application status: pending, accepted, or rejected",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "Yaw Mensah",
                "email": "yawmensah@gmail.com",
                "phone": "0558876123",
                "university": "KNUST",
                "course": "Electrical Engineering",
                "level": "4th Year",
                "track": "Radar & RF Systems",
                "motivation": "Updated motivation statement focusing on antenna arrays and satellite RF.",
                "portfolio_link": "https://github.com/yawmensah",
                "resume_link": "https://linkedin.com/in/yawmensah",
                "join_innovation_club": True,
                "status": "accepted",
            }
        }
    )


class ApplicationStatusUpdate(BaseModel):
    """Schema for updating application status only."""
    status: ApplicationStatus = Field(
        ...,
        description="Updated status: pending, accepted, or rejected",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "accepted"
            }
        }
    )


class ApplicationResponse(BaseModel):
    """Complete application response schema."""
    id: int = Field(..., description="Unique application identifier")
    full_name: str = Field(..., description="Full applicant name")
    email: str = Field(..., description="Applicant email address")
    phone: str = Field(..., description="Phone / WhatsApp contact number")
    university: Optional[str] = Field(None, description="University name")
    course: Optional[str] = Field(None, description="Course / field of study")
    level: Optional[str] = Field(None, description="Academic level")
    track: Optional[str] = Field(None, description="Selected specialization track")
    motivation: Optional[str] = Field(None, description="Motivation statement")
    portfolio_link: Optional[str] = Field(None, description="Portfolio URL")
    resume_link: Optional[str] = Field(None, description="Resume URL")
    join_innovation_club: Optional[bool] = Field(None, description="Innovation club membership intent")
    status: Optional[str] = Field(None, description="Application review status")
    submitted_at: Optional[str] = Field(None, description="ISO-8601 submission timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
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
                "join_innovation_club": True,
                "status": "pending",
                "submitted_at": "2026-05-05T08:45:30Z",
            }
        }
    )
