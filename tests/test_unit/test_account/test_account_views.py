import pytest
from tests.utils import *
from account.views.account import UserSignupView, UserLoginView
from unittest.mock import patch


@pytest.fixture
def user_signup_view():
    view = UserSignupView()
    return view

@pytest.mark.django_db
@pytest.mark.parametrize(
    "email, password, status",
    [
        ('test@test.com', 'test', 200),
        ('test123@test.com', 'test', 200),
        ('test@test.com', '@312', 200),
        ('@test123@test.com', 'test', 400),
        ('test', 'test', 400),
        ('', '', 400)
    ]
)
def test_user_signup_view(user_signup_view, email, password, status):
    data = {'email': email, 'password': password}
    request = httprequest_for_signup(method='POST', data=data)
    response = user_signup_view.post(request)
    assert response.status_code == status
    if status == 200:
        assert response.data['data']['email']
        assert response.data['data']['password']



@pytest.fixture
def user_login_view():
    view = UserLoginView()
    return view

@pytest.mark.parametrize(
    "email, password, status",
    [
        ('test@test.com', 'test', 202),
        ('test', 'test', 400)
    ]
)
@patch('account.views.account.authenticate')
@pytest.mark.django_db
def test_user_login_view(mock_authenticate, user_login_view, email, password, status):
    # Mocking
    mock_authenticate.return_value = EmailSignupFactory(email='test@test.com', password='test')
    
    # Create request
    request = httprequest_for_login('POST', {'email': email, 'password': password})
    
    # Call the view
    response = user_login_view.post(request)
    
    # Assertions
    assert response.status_code == status
    if status == 202:
        assert response.data['data']['access_token']
        assert response.data['data']['refresh_token']
