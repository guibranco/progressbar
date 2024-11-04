import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_dashboard_route(client):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Activity Dashboard is under construction.' in response.data

def test_redirect_to_github(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == 'https://github.com/guibranco/progressbar'
