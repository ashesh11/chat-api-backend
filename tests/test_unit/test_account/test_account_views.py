import pytest
from tests.utils import *
from account.views.account import UserSignupView, UserLoginView


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

@pytest.mark.django_db
@pytest.mark.parametrize(
    'email, password, status',
    [
        ('test@test.com', 'test', 202)
    ]
)
def test_user_login_view(user_login_view, email, password, status):
    data = {'email': email, 'password': password}
    request = httprequest_for_login(method='POST', data=data)
    response = user_login_view.post(request)
    assert response.status_code == status