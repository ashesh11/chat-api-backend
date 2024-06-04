import pytest
from tests.dummy_data.account import EmailSignupFactory
from account.views.token import RefreshTokenView
from account.utils import generate_refresh_token
from tests.utils import *


@pytest.fixture
def token_refresh_view():
    view = RefreshTokenView()
    return view

@pytest.mark.django_db
def test_token_refresh_view(token_refresh_view):
    user = EmailSignupFactory()
    refresh_token = generate_refresh_token(user)
    request = httprequest_for_login(method='POST', data={'refresh_token': refresh_token})
    response = token_refresh_view.post(request)

    assert response.status_code == 201
    assert response.data['data'].get('access_token')