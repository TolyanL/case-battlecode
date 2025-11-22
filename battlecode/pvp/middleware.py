from django.utils import timezone

from battlecode.redis_settings import client
from battlecode.pvp_settings import REDIS_TTL


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cache_key = f"user-last-active-{request.user.id}"
            client.setex(cache_key, REDIS_TTL, timezone.now().timestamp())

        response = self.get_response(request)
        return response
