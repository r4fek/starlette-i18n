import pytest
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_i18n import (
    LocaleDefaultMiddleware,
    LocaleFromCookieMiddleware,
    LocaleFromHeaderMiddleware,
    get_locale_code,
    load_gettext_translations,
)

from . import constants, messages


@pytest.fixture()
def load_translations():
    load_gettext_translations(directory=constants.BABEL_LOCALES_PATH, domain=constants.BABEL_DOMAIN)


def success(request):
    return PlainTextResponse(messages.SUCCESS, status_code=200)


def locale_code(request):
    return PlainTextResponse(get_locale_code(), status_code=200)


def error(request):
    return PlainTextResponse(messages.ERROR, status_code=500)


@pytest.fixture()
def app(load_translations):
    app_ = Starlette(
        routes=[
            Route("/success/", success),
            Route("/locale/", locale_code),
            Route("/error/", error),
        ],
    )
    app_.add_middleware(LocaleFromHeaderMiddleware)
    app_.add_middleware(LocaleFromCookieMiddleware)
    app_.add_middleware(LocaleDefaultMiddleware, default_code="en")
    return app_


@pytest.fixture
def client(app):
    return TestClient(app)
