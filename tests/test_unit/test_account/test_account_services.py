import pytest
from account.services.account import UserAccountServices
from tests.dummy_data.account import EmailSignupFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email, password",
    [
        ('test@test.com', 'test'),
        ('test', 'test'),
        ('', '')
    ]
)
def test_account_service_create(email, password):
    data = {'email': email, 'password': password}
    user, error = UserAccountServices.create(data=data)
    if user:
        assert user.email == email
    if error:
        assert 'User account creation failed.' in error.get('error')


@pytest.mark.django_db
def test_account_service_list_active_users():
    # Testing without any users present
    users, error = UserAccountServices.list_active_users()
    assert users == None
    assert 'No active users' in error.get('error')

    # Creating 5 dummy users
    for i in range(5):
        EmailSignupFactory(id=i, email=f'test{i}@test.com', password='test')

    # Testing with dummy users present
    users, error = UserAccountServices.list_active_users()

    assert users.count() == 5
    assert error == None


@pytest.mark.django_db
def test_account_service_retrieve_active_user():
    # Testing without user present
    user, error = UserAccountServices.retrieve_active_user(user_id=1)
    assert user == None
    assert 'User not found' in error.get('error')

    # Creating dummy user with id 1
    EmailSignupFactory(id=1)

    # Testing with that user present
    user, error = UserAccountServices.retrieve_active_user(user_id=1)
    assert user.id == 1
    assert error == None