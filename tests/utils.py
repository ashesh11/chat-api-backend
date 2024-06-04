from django.http import HttpRequest
from tests.dummy_data.account import EmailSignupFactory


def httprequest_for_signup(method, data=None):
    request = HttpRequest()
    request.method = method
    request.data = data
    return request

def httprequest_for_login(method, data=None):
    request = HttpRequest()
    request.method = method
    request.data = data
    return request