from django.conf import settings

from root_logging import MODULE_NAME

FILE_NAME = 'middleware'


class LoggingMiddleware(object):
    """ Only last middleware in MIDDLEWARE list! """

    class_name = 'LoggingMiddleware'
    middleware_path = MODULE_NAME + '.' + FILE_NAME + '.' + class_name

    def __init__(self, get_response):
        if len(settings.MIDDLEWARE) > 1 and self.middleware_path not in settings.MIDDLEWARE[-1]:
            raise IndexError('LoggingMiddleware must be last in the MIDDLEWARE list')

        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)

        url = None

        if hasattr(request.resolver_match, 'view_name'):
            url = request.resolver_match.view_name
        elif request.META.get('HTTP_REFERER', None):
            url = request.META['HTTP_REFERER']

        settings.LOGGER.log.debug('Response from `{}`. Request: `{}`. Response Code: `{}`'.format(
                url,
                request.method,
                response.status_code
            )
        )

        return response

    @staticmethod
    def process_exception(request, exception):
        settings.LOGGER.log.critical(exception, exc_info=True)
