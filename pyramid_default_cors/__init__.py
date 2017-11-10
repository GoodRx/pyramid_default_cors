"""
Preflight approach inspired by
# https://gist.github.com/kamalgill/b1f682dbdc6d6df4d052
# MIT License Protected code
"""

def add_cors_to_response(event):
    request = event.request
    response = event.response
    if 'Origin' in request.headers:
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']


def cors_options_view(context, request):
    response = request.response
    if 'Access-Control-Request-Headers' in request.headers:
        response.headers['Access-Control-Allow-Methods'] = ', '.join({
            'POST',
            'PUT',
            'DELETE',
        })
    response.headers['Access-Control-Allow-Headers'] = ', '.join({
        'Content-Type',
        'Accept',
        'X-Requested-With',
    })
    request.response.headers['Access-Control-Max-Age'] = '3600'

    return response


class CorsPreflightPredicate(object):
    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'cors_preflight = %s' % bool(self.val)

    # Predicate Hash
    phash = text

    def __call__(self, context, request):
        if not self.val:
            return False
        return (
            request.method == 'OPTIONS' and
            'Origin' in request.headers and
            'Access-Control-Request-Method' in request.headers
        )


def includeme(config):
    config.add_route_predicate('cors_preflight', CorsPreflightPredicate)
    config.add_subscriber(add_cors_to_response, 'pyramid.events.NewResponse')

    config.add_route(
        'cors-options-preflight', '/{catch_all:.*}',
        cors_preflight=True,
    )
    config.add_view(
        cors_options_view,
        route_name='cors-options-preflight',
    )
