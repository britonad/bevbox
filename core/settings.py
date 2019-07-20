import os

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')


class Common:
    """Common settings class. All children inherit from this one."""

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(BASE_DIR, 'translations')
    BABEL_DEFAULT_LOCALE = 'uk'
    TELEGRAM_API_URL = 'https://api.telegram.org'
    LANGUAGES = {
        'en': 'En',
        'uk': 'Uk',
        'ru': 'Ru'
    }


class Dev(Common):
    """Development settings for local development."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:root@localhost/bevbox'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    CHANNEL_ID = ''
    BOT_TOKEN = ''
    MAILGUN_API_KEY = ''
    EMAIL_RECIPIENT = ''
    MAILGUN_DOMAIN_NAME = ''
    CREDIT_CARD = ''


class Testing(Common):
    """Testing settings."""

    DEBUG = True
    TESTING = True

    # Alchemy settings.
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

    # Telegram settings.
    CHANNEL_ID = ''
    BOT_TOKEN = ''

    # Mailgun settings.
    MAILGUN_API_KEY = ''
    MAILGUN_DOMAIN_NAME = ''
    EMAIL_RECIPIENT = ''

    # Credit card
    CREDIT_CARD = '5411 1111 1111 1111'

    # WTForms settings.
    WTF_CSRF_ENABLED = False


class Prod(Common):
    """Product settings."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CHANNEL_ID = os.environ.get('CHANNEL_ID')
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    MAILGUN_DOMAIN_NAME = os.environ.get('MAILGUN_DOMAIN_NAME')
    EMAIL_RECIPIENT = os.environ.get('EMAIL_RECIPIENT')
    CREDIT_CARD = os.environ.get('CREDIT_CARD')
