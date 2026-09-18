"""In-memory mock dataset for applications.

This module provides the initial seed data and a factory function to obtain
a fresh copy of mock applications without using a persistent database.
"""

from typing import Any, Dict, List
import copy


INITIAL_MOCK_APPLICATIONS: List[Dict[str, Any]] = [
    {
        "id": 2,
        "full_name": "Ama Serwaa Owusu",
        "email": "amaserwaa@gmail.com",
        "phone": "0245567812",
        "university": None,
        "course": None,
        "level": None,
        "track": None,
        "motivation": None,
        "portfolio_link": None,
        "resume_link": None,
        "join_innovation_club": None,
        "status": None,
        "submitted_at": None,
    },
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
        "join_innovation_club": True,
        "status": "pending",
        "submitted_at": "2026-05-05T08:45:30Z",
    },
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
        "join_innovation_club": True,
        "status": "accepted",
        "submitted_at": "2026-05-06T14:18:22Z",
    },
    {
        "id": 5,
        "full_name": "Daniel Kofi Asante",
        "email": "danielasante@gmail.com",
        "phone": "0277788990",
        "university": "UENR",
        "course": "Biomedical Engineering",
        "level": "2nd Year",
        "track": "Biomedical Systems",
        "motivation": "To explore biomedical monitoring systems and healthcare technology innovations.",
        "portfolio_link": "https://github.com/danielasante",
        "resume_link": "https://linkedin.com/in/danielasante",
        "join_innovation_club": False,
        "status": "rejected",
        "submitted_at": "2026-05-07T11:05:10Z",
    },
]


def get_initial_mock_applications() -> List[Dict[str, Any]]:
    """Return a deep copy of the initial mock dataset."""
    return copy.deepcopy(INITIAL_MOCK_APPLICATIONS)
