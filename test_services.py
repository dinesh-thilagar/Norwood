from fastapi.testclient import TestClient
from fastapi import FastAPI
from services import app


def get_test_app():
    # Create a test app by wrapping the main FastAPI app
    test_app = FastAPI()
    test_app.mount("/", app)
    return test_app


client = TestClient(get_test_app())


def test_configure_loopback():
    response = client.post(
        "/configure_loopback/",
        json={
            "loopback_num": 1,
            "description": "Test Loopback",
            "ipv4_address": "192.168.1.1",
            "subnet_mask": "255.255.255.0"
        }
    )
    assert response.status_code == 200
    # assert response.json()["message"] == "Loopback configured successfully"
    # assert "Loopback0" in response.json()["output"]

# def test_delete_loopback():
#     response = client.delete("/delete_loopback/")
#     assert response.status_code == 200
#     assert response.json()["message"] == "Loopback deleted successfully"
