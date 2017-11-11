from pretend import stub
from pyramid.testing import DummyRequest
import pytest

from pyramid_default_cors import add_cors_to_response
from pyramid_default_cors import cors_options_view
from pyramid_default_cors import CorsPreflightPredicate
from pyramid_default_cors import includeme


@pytest.mark.parametrize('val', [True, False])
@pytest.mark.parametrize('is_option', [True, False])
@pytest.mark.parametrize('has_origin', [True, False])
@pytest.mark.parametrize('has_access_control', [True, False])
def test_cors_conditions(val, is_option, has_origin, has_access_control):
    predicate = CorsPreflightPredicate(val, None)
    request = DummyRequest()
    if is_option:
        request.method = 'OPTIONS'
    if has_origin:
        request.headers['Origin'] = 'hello'
    if has_access_control:
        request.headers['Access-Control-Request-Method'] = 'goodbye'

    do_preflight = predicate(None, request)

    if all([val, is_option, has_origin, has_access_control]):
        assert do_preflight is True
    else:
        assert do_preflight is False


@pytest.mark.parametrize('has_origin', [True, False])
def test_adds_cors_response(has_origin):
    request = DummyRequest()
    response = DummyRequest()
    event = stub(request=request, response=response)
    if has_origin:
        request.headers['Origin'] = 'hello'

    add_cors_to_response(event)

    if has_origin:
        assert (
            event.response.headers['Access-Control-Allow-Origin']
            == event.request.headers['Origin']
        )
    else:
        assert 'Access-Control-Allow-Origin' not in event.response.headers


@pytest.mark.parametrize('has_access_control', [True, False])
def test_adds_response_headers(has_access_control):
    request = DummyRequest()
    if has_access_control:
        request.headers['Access-Control-Request-Headers'] = 'hello'

    response = cors_options_view(None, request)

    if has_access_control:
        assert (
            set(response.headers['Access-Control-Allow-Methods'].split(', '))
            == {'PUT', 'POST', 'DELETE'}
        )
    else:
        assert 'Access-Control-Allow-Methods' not in response.headers
    assert (
        set(response.headers['Access-Control-Allow-Headers'].split(', '))
        == {'Content-Type', 'Accept', 'X-Requested-With'}
    )
    assert response.headers['Access-Control-Max-Age'] == '3600'


def test_proper_setup(mocker):
    """ Probably a better way to test this is to setup a test web app. """
    config = mocker.patch('pyramid.config.Configurator')

    includeme(config)

    assert config.add_route_predicate.call_args[0][0] == 'cors_preflight'
    assert config.add_route_predicate.call_args[0][1] == CorsPreflightPredicate

    assert config.add_subscriber.call_args[0][0] == add_cors_to_response
    assert config.add_subscriber.call_args[0][1] == 'pyramid.events.NewResponse'

    assert config.add_route.call_args[0][0] == 'cors-options-preflight'
    assert config.add_route.call_args[0][1] == '/{catch_all:.*}'
    assert config.add_route.call_args[1] == {'cors_preflight': True}

    assert config.add_view.call_args[0][0] == cors_options_view
    assert config.add_view.call_args[1] == {'route_name': 'cors-options-preflight'}
