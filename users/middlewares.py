from .models import RequestLog


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if str(request.path).startswith(('/admin', '/favicon.ico')):
            response = self.get_response(request)
            return response
        request_log = RequestLog.objects.create(
            ip_address=request.META.get('REMOTE_ADDR'),
            referer=request.META.get('HTTP_REFERER'),
            user_agent=request.headers.get('User-Agent'),
            url=request.path,
            method=request.method)
        request_log.save()

        response = self.get_response(request)

        if request.user.is_authenticated:
            request_log.user = request.user
            request_log.save()

        return response
