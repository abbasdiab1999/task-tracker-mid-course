import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import storage


@pytest.fixture(autouse=True)
def clean_storage():
    storage.reset_storage()


@pytest.fixture
def client():
    return TestClient(app)
