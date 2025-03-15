from articles.redis import get_redis_client


class StatMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        redis = get_redis_client()
        redis.incr(f"stat_{request.path}")
        return response