from csp.middleware import CSPMiddleware as CSPMiddlewareBase


class CSPMiddleware(CSPMiddlewareBase):
    """CSPMiddleware, which is only activated for non-staff users"""
    def process_request(self, request):
        if request.user.is_staff:
            return None
        return super(CSPMiddleware, self).process_request(request)

    def process_response(self, request, response):
        if request.user.is_staff:
            return response
        return super(CSPMiddleware, self).process_response(request, response)
