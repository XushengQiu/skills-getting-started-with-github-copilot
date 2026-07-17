import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as app_activities


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_activities():
    app_activities.clear()
    app_activities.update(
        copy.deepcopy(
            {
                "Chess Club": {
                    "description": "Learn strategies and compete in chess tournaments",
                    "schedule": "Fridays, 3:30 PM - 5:00 PM",
                    "max_participants": 12,
                    "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
                },
                "Programming Class": {
                    "description": "Learn programming fundamentals and build software projects",
                    "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                    "max_participants": 20,
                    "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
                },
                "Gym Class": {
                    "description": "Physical education and sports activities",
                    "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                    "max_participants": 30,
                    "participants": ["john@mergington.edu", "olivia@mergington.edu"],
                },
                "Soccer Club": {
                    "description": "Team practices, drills, and intramural matches",
                    "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                    "max_participants": 22,
                    "participants": ["alek@mergington.edu", "marco@mergington.edu"],
                },
                "Swimming Team": {
                    "description": "Lap training, stroke technique, and competitive meets",
                    "schedule": "Mondays, Wednesdays, 5:00 PM - 6:30 PM",
                    "max_participants": 18,
                    "participants": ["nina@mergington.edu"],
                },
                "Art Club": {
                    "description": "Drawing, painting, and mixed-media workshops",
                    "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
                    "max_participants": 25,
                    "participants": ["lucy@mergington.edu", "harper@mergington.edu"],
                },
                "School Band": {
                    "description": "Instrument practice, ensemble rehearsals, and performances",
                    "schedule": "Fridays, 4:00 PM - 6:00 PM",
                    "max_participants": 40,
                    "participants": ["peter@mergington.edu", "isla@mergington.edu"],
                },
                "Debate Team": {
                    "description": "Learn argumentation, public speaking, and compete in debates",
                    "schedule": "Thursdays, 3:30 PM - 5:00 PM",
                    "max_participants": 16,
                    "participants": ["sara@mergington.edu"],
                },
                "Science Club": {
                    "description": "Hands-on experiments, research projects, and science fairs",
                    "schedule": "Mondays, 3:30 PM - 5:00 PM",
                    "max_participants": 20,
                    "participants": ["kevin@mergington.edu", "maya@mergington.edu"],
                },
            }
        )
    )
    yield


def test_get_activities_returns_available_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert response.json()["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_adds_new_participant(client):
    response = client.post("/activities/Chess Club/signup?email=student@example.com")

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up student@example.com for Chess Club"

    activities_response = client.get("/activities")
    assert "student@example.com" in activities_response.json()["Chess Club"]["participants"]


def test_signup_for_existing_participant_returns_400(client):
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_for_activity_removes_participant(client):
    response = client.delete("/activities/Chess Club/unregister?email=michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    assert "michael@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]
