import os

import sentry_sdk
from flask import abort, Flask, g, request, render_template
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sentry_sdk.integrations.flask import FlaskIntegration

try:
    from core import local_settings as settings
except ImportError:
    from core import settings

__version__ = '1.0.0'


babel = Babel()
db = SQLAlchemy()
migration = Migrate()


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

    # Load configuration.
    environment = os.environ.get('APP_ENV', 'dev')
    environments = {
        'dev': settings.Dev,
        'prod': settings.Prod
    }
    if environment in environments:
        application.config.from_object(environments[environment])
    else:
        raise EnvironmentError('Application variable has not been specified.')

    # Initialize third-party libs.
    babel.init_app(application)
    db.init_app(application)
    migration.init_app(application, db)

    # Initialize sentry integration.
    sentry_sdk.init(integrations=[FlaskIntegration()])

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

    @application.errorhandler(404)
    def not_found(error):
        lang = request.path.split('/')[1].lower()
        if lang and lang in application.config['LANGUAGES'].keys():
            g.lang = lang
        else:
            g.lang = 'uk'

        return render_template('404.html'), 404

    # Register blueprints
    from admin.views import admin_bp
    from app.views import app_bp

    application.register_blueprint(admin_bp)
    application.register_blueprint(app_bp)
    application.register_blueprint(app_bp, url_prefix='/<lang>')

    return application
