from http import HTTPStatus

import pytest

from core import create_app


def test_app_wrong_env(monkeypatch):
    # Given: not existing env set as a env variable in a system.
    monkeypatch.setenv('APP_ENV', 'wrong_env')

    # When: we create an instance of the app with this env.
    # Then: we receive EnvironmentError.
    with pytest.raises(EnvironmentError):
        create_app()


def test_home_page_uk(client):
    # Given: Ukrainian language is set by default.
    # When: we send a request.
    response = client.get('/')

    # Then: we receive a successful response with Ukrainian translation.
    assert response.status_code == HTTPStatus.OK
    assert 'смак' in response.data.decode('utf-8', 'replace')


def test_home_page_ru(client):
    # Given: Russian language is provided.
    # When: we send a request.
    response = client.get('/ru/')

    # Then: we receive a successful response with Russian translation.
    assert response.status_code == HTTPStatus.OK
    assert 'вкус' in response.data.decode('utf-8', 'replace')


def test_home_page_en(client):
    # Given: English language is provided.
    # When: we send a request.
    response = client.get('/en/')

    # Then: we receive a successful response with English translation.
    assert response.status_code == HTTPStatus.OK
    assert b'flavor' in response.data


def test_wrong_translation_lang(client):
    # Given: Spanish language is provided.
    # When: we send a request.
    response = client.get('/es/')

    # Then: we receive 404 with a default language (Ukrainian).
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'Сторінка не найдена' in response.data.decode('utf-8', 'replace')


def test_wrong_translation_lang_that_user_used(client):
    # Given: A user was surfing pages in English language.
    response = client.get('/en/')
    assert response.status_code == HTTPStatus.OK
    assert b'flavor' in response.data

    # When: The user jumped to a wrong URL.
    response = client.get('/en/wrong/')

    # Then: he'll receive 404 error in English.
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert b'Page not found' in response.data


def test_success_page(client):
    # Given: a user placed an order and will be redirected to the success
    # page.
    # When: the user send a request.
    response = client.get('/en/success/')

    # Then: a success message will appear.
    assert response.status_code == HTTPStatus.OK
    assert b'Thank you' in response.data


def test_email_success_page(client):
    # Given: a user filled a message from contact form.
    # When: the user send a request.
    response = client.get('/en/email-success/')

    # Then: the user will see feed on it.
    assert response.status_code == HTTPStatus.OK
    assert b'delivered to us' in response.data


def test_maintenance(client):
    # Given: Bevbox is down.
    # When: a user sends a request.
    response = client.get('/en/maintenance/')

    # Then: a maintenance appears.
    assert response.status_code == HTTPStatus.OK
    assert b'Stay tuned.' in response.data


def test_privacy_policy(client):
    # Given: a user navigates privacy policy page.
    # When: the user sends a request.
    response = client.get('/en/privacy-policy/')

    # Then: privacy policy shows.
    assert response.status_code == HTTPStatus.OK
    assert b'page informs you of our policies' in response.data


def test_terms_of_use(client):
    # Given: a user navigates terms of use page.
    # When: the user sends a request.
    response = client.get('/en/terms-of-use/')

    # Then: terms of use shows.
    assert response.status_code == HTTPStatus.OK
    assert b'These Terms of Use outline the rules' in response.data


def test_refund_policy(client):
    # Given: a user navigates refund policy page.
    # When: the user sends a request.
    response = client.get('/en/refund-policy/')

    # Then: refund policy shows.
    assert response.status_code == HTTPStatus.OK
    assert b'Our refund policy' in response.data


def test_contact_form(client):
    # Given: a user navigates a contact form.
    # When: the user sends a request.
    response = client.get('/en/contacts/')

    # Then: contacts shows.
    assert response.status_code == HTTPStatus.OK
    assert b'bevbox.com.ua@gmail.com' in response.data


def test_subscription_form(client):
    # Given: a user navigates a subscription form.
    # When: the user sends a request.
    response = client.get('/en/subscription/')

    # Then: subscription form shows.
    assert response.status_code == HTTPStatus.OK
    assert b'Payment option' in response.data
