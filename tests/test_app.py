import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("participants" in v for v in data.values())


def test_signup_for_activity():
    # Use a test email and activity
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(iter(activities.keys()))
    email = "pytest@example.com"
    signup_url = f"/activities/{activity_name}/signup?email={email}"
    response = client.post(signup_url)
    assert response.status_code == 200
    # Try to sign up again (should fail or return error)
    response2 = client.post(signup_url)
    assert response2.status_code != 200 or response2.json().get("detail")


def test_unregister_for_activity():
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(iter(activities.keys()))
    email = "pytest@example.com"
    signup_url = f"/activities/{activity_name}/signup?email={email}"
    unregister_url = f"/activities/{activity_name}/unregister?email={email}"
    # Ensure signed up
    client.post(signup_url)
    # Unregister
    response = client.post(unregister_url)
    assert response.status_code == 200
    # Unregister again (should fail or return error)
    response2 = client.post(unregister_url)
    assert response2.status_code != 200 or response2.json().get("detail")
