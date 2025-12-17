from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Mergington High School" in resp.text


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_adds_participant():
    activity = "Chess Club"
    email = "tester@example.com"

    # Ensure not already signed up
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    if email in data[activity]["participants"]:
        # remove if present to ensure test idempotence
        data[activity]["participants"].remove(email)

    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    body = signup_resp.json()
    assert "Signed up" in body.get("message", "")

    # Verify participant was added
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert email in data2[activity]["participants"]
