import pytest
import json
import sys
sys.path.append("..")
from app.views import app


@pytest.fixture
def client():
    test_client = app.test_client()
    return test_client

@pytest.fixture
def sample_user():
    test_user = {
        "admin": 'false',
        "email": "maryn@gmail.com",
        "name": "kiki","password": "pass",
        "use_id":1,
        "username":"maymay"

    }
    return test_user
def test_api_registeruser(client,sample_user):
    response = 

