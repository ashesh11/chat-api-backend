from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from account.models.token import BlacklistedToken

class CheckBlacklistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[-1]
        if BlacklistedToken.objects.filter(token=token).exists():
            return HttpResponseForbidden("Your token has been blacklisted.")
