import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client):
    client = APIClient()

    # Create Test User
    User = get_user_model()
    User.objects.create_user(email="test@user.com", password="testuser")

    # Sign Up using test user credentials
    signup_credentials = {
        "email": "test@user.com",
        "password": "testuser"
    }
    url = reverse('user-signup')
    api_client.post(url, data=signup_credentials)

    # Login using test user
    login_credentials = {
        "email": "test@user.com",
        "password": "testuser"
    }
    url = reverse('user-login')
    response = api_client.post(url, data=login_credentials)

    access_token = response.json()["access_token"]

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    client.force_authenticate(user=User.objects.first())

    return client