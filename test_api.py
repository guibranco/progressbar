import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_svg_response(client):
    response = client.get("/28/")

    assert response.status_code == 200

    assert response.content_type == "image/svg+xml"

    assert b"<svg" in response.data
    assert b"</svg>" in response.data
