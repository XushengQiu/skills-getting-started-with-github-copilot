from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    response = client.post(
        "/activities/Chess Club/signup?email=student@example.com"
    )
    assert response.status_code == 200

    response = client.delete("/activities/Chess Club/unregister?email=student@example.com")
    assert response.status_code == 200
    assert response.json()["message"] == "Removed student@example.com from Chess Club"

    activity_response = client.get("/activities")
    activities = activity_response.json()["Chess Club"]
    assert "student@example.com" not in activities["participants"]
