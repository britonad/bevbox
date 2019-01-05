import os

from flask import abort, Flask, g
from flask_babel import Babel

try:
    from core import local_settings as settings
except ImportError:
    from core import settings

__version__ = '1.0.0'


babel = Babel()


def create_app() -> Flask:
    """
    This function creates application with predefined settings that depends on
    environment variable of a system.
    """

    application = Flask(
        __name__,
        template_folder=settings.TEMPLATE_DIR,
        static_folder=settings.STATIC_DIR
    )
    environment = os.environ.get('APP_ENV', 'dev')
    environments = {
        'dev': settings.Dev,
        'prod': settings.Prod
    }
    if environment in environments:
        application.config.from_object(environments[environment])
    else:
        raise EnvironmentError('Application variable has not been specified.')

    babel.init_app(application)

    @babel.localeselector
    def get_locale():
        return g.get('lang', application.config['BABEL_DEFAULT_LOCALE'])

    @application.url_defaults
    def set_language_code(endpoint, values):
        if 'lang' in values or not g.get('lang', None):
            return
        if application.url_map.is_endpoint_expecting(endpoint, 'lang'):
            values['lang'] = g.lang

    @application.url_value_preprocessor
    def get_language_code(endpoint, values):
        if values is not None:
            g.lang = values.pop('lang', None)

    @application.before_request
    def ensure_language_support():
        lang = g.get('lang', None)
        if lang and lang not in application.config['LANGUAGES'].keys():
            return abort(404)

    # Register blueprints
    from app.views import app_bp
    application.register_blueprint(app_bp)
    application.register_blueprint(app_bp, url_prefix='/<lang>')

    return application
