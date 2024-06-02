from django.http import JsonResponse
from account.models.token import BlacklistedToken

class CheckBlacklistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[-1]
        if BlacklistedToken.objects.filter(token=token).exists():
            return JsonResponse({"error":"Token has been blacklisted."}, status=403)
        
        # If the token is not blacklisted, proceed with the next middleware or view
        response = self.get_response(request)
        return response
