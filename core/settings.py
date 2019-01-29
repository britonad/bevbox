import os

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')


class Common:
    """
    Common settings class. All children inherit from this one.
    """

    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(BASE_DIR, 'translations')
    BABEL_DEFAULT_LOCALE = 'uk'
    LANGUAGES = {
        'en': 'En',
        'uk': 'Uk',
        'ru': 'Ru'
    }


class Dev(Common):
    """
    Development settings for local development.
    """

    DEBUG = True
    TESTING = True
    MERCHANT_LOGIN = 'test_merch_n1'
    MERCHANT_SECRET_KEY = 'flk3409refn54t54t*FNJRET'


class Prod(Common):
    """
    Product settings.
    """

    DEBUG = False
    MERCHANT_LOGIN = os.environ.get('MERCHANT_LOGIN')
    MERCHANT_SECRET_KEY = os.environ.get('MERCHANT_SECRET_KEY')
