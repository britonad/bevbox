from collections import namedtuple
from http import HTTPStatus
from unittest import mock

import pytest
from flask import session

from app.forms import SubscriptionForm
from app.models import Order
from app.utils import (
    calculate_subscription_cost,
    create_invoice_msg,
    create_order_notification_msg,
    get_price,
    get_subscription_name,
    send_email,
    send_message_to_channel,
    send_invoice
)
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
    # Given: A user is surfing pages in English language.
    response = client.get('/en/')
    assert response.status_code == HTTPStatus.OK
    assert b'flavor' in response.data

    # When: The user jumps to a wrong URL.
    response = client.get('/en/wrong/')

    # Then: he receives 404 error in English.
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert b'Page not found' in response.data


@mock.patch('app.utils.requests.post')
@mock.patch('app.utils.requests.get')
@mock.patch('app.views.deepcopy')
def test_place_an_order(
        mock_deepcopy, mock_get, mock_post, app, client, order_data
):
    # Given: a subscription form data.
    mock_deepcopy.return_value = order_data  # A hacky way to bypass CSRF PITA.

    # When: a user sends a request.
    response = client.post(
        '/en/subscription/', data=order_data, follow_redirects=True
    )

    # Then: we receives Telegram notification, the use gets an invoice,
    # and an order creates in a DB.
    with app.app_context():
        assert Order.query.first()
    assert mock_get.called_once
    assert mock_post.called_once
    assert response.status_code == HTTPStatus.OK


@mock.patch('app.utils.requests.post')
def test_feedback_form(mock_post, app, client):
    data = {
        'email': 'tester@test.com',
        'subject': 'Test sbj.',
        'name': 'John',
        'message': 'Testing.'
    }
    response = client.post('/en/contacts/', data=data, follow_redirects=True)
    
    assert mock_post.called_once
    assert response.status_code == HTTPStatus.OK


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


def test_subscription_form_checked_fields(client):
    # Given: a user submits a subscription form with  all checked checkboxes.
    data = {
        'stones': True,
        'cigar': True,
        'matches': True,
        'guillotine': True
    }
    stones = (
        '<input checked class="t-checkbox js-tilda-rule" id="stones" '
        'name="stones" style="color: #F95D51" type="checkbox" value="True">'
    ).encode()
    cigar = (
        '<input checked class="t-checkbox js-tilda-rule" id="cigar" '
        'name="cigar" style="color: #F95D51" type="checkbox" value="True">'
    ).encode()
    matches = (
        '<input checked class="t-checkbox js-tilda-rule" id="matches" '
        'name="matches" style="color: #F95D51" type="checkbox" value="True">'
    ).encode()
    guillotine = (
        '<input checked class="t-checkbox js-tilda-rule" id="guillotine" '
        'name="guillotine" style="color: #F95D51" type="checkbox" '
        'value="True">'
    ).encode()

    # When: the user presses a button.
    response = client.post('/en/subscription/', data=data)

    # Then: all checkboxes rendered properly.
    assert response.status_code == HTTPStatus.OK
    assert stones in response.data
    assert cigar in response.data
    assert matches in response.data
    assert guillotine in response.data


def test_order_repr_string():
    # Given: a dummy e-mail provided.
    email = 'dummy@host.com'
    order = Order(email=email)
    representation = f'<Order {email}-None>'

    # When: repr function invokes.
    # Then: it should coincide with representation variable.
    assert repr(order) == representation


def test_get_price():
    # Given: a subscription type junior picked.
    # When: we pass it to get_price function.
    # Then: it should be equal to 2391.
    assert get_price(SubscriptionForm.JUNIOR) == 2391


def test_get_subscription_name(app):
    # Given: a subscription type senior picked with the default language.
    # When: we pass the subscription name to get_subscription_name function
    # that wrapped by the app context.
    with app.app_context():

        # Then: it should be equal to "Дебютант" value.
        assert get_subscription_name(SubscriptionForm.SENIOR) == 'Шанувальник'


def test_calculate_senior_subscription_cost(order_data):
    # Given: an order data that specifies to skip cigar, stones, matches &
    # guillotine for a senior subscription type.
    # When: a function is invoked.
    # Then: the calculations of costs happens and the output is a number 3965.
    assert calculate_subscription_cost(order_data) == 3965


def test_calculate_middle_subscription_cost(order_data):
    # Given: an order data that specifies to skip cigar, stones, matches &
    # guillotine for a middle subscription type.
    order_data['subscription_type'] = SubscriptionForm.MIDDLE

    # When: a function is invoked.
    # Then: the calculations of costs happens and the output is a number 2882.
    assert calculate_subscription_cost(order_data) == 2882


def test_calculate_junior_subscription_cost(order_data):
    # Given: an order data that specifies to skip cigar, stones, matches &
    # guillotine for a junior subscription type.
    order_data['subscription_type'] = SubscriptionForm.JUNIOR

    # When: a function is invoked.
    # Then: the calculations of costs happens and the output is a number 1561.
    assert calculate_subscription_cost(order_data) == 1561


def test_create_invoice_msg(app, order_data):
    # Given: an order data that specifies to skip cigar, stones, matches &
    # guillotine for a senior subscription type.
    output_message = '<p>Любий, Tester.</p>\n<p>\n  Дякуємо, за вибір типа підписки "Шанувальник".\n<p><b> Загальна сума до сплати:</b> ₴3965.</p>\n<p><b>Номер кредитної карти:</b> 5411 1111 1111 1111.</p>'

    # When: the order data passed to a function.
    with app.app_context():
        # Then: the function output should coincide with the output_message.
        assert create_invoice_msg(order_data) == output_message


def test_create_order_notification_msg(order_data):
    # Given: a client placed an order.
    order = namedtuple('Order', ['id'])

    # When: the client hits the submit button.
    result = create_order_notification_msg(order(id=1), order_data)
    output_message = 'Замовлення <b>№1</b>.\nКлієнт <b>Tester</b> з міста <b>Kyiv</b> замовив підписку <b>senior</b> у відділення "Нової Пошти" <b>№1</b>.\nEmail: <a href="mailto:tester@test.com">tester@test.com</a>\nТелефон: <a href="tel:+380123456789">+380123456789</a>\nВаріант оплати: <b>cc</b>\nСигара: <b>ні</b>\nСірники: <b>ні</b>\nКаміньці: <b>ні</b>\nГільйотина: <b>ні</b>\nПобажання: <b>Немає</b>\n\n<b>Вартість</b>: <i>₴3965</i>'

    # Then: we get Telegram notification.
    assert result == output_message


@mock.patch('app.utils.requests.post')
def test_send_email(mock_post, app):
    # Given: attrs for an function.
    calls = [
        mock.call(
            'https://api.mailgun.net/v3//messages',
            auth=('api', ''),
            data={
                'from': 'test <tester@test.com>',
                'to': '',
                'subject': 'Test',
                'text': 'Test message.'
            }
        )
    ]

    # When: the attrs passed to the function.
    with app.app_context():
        # Then: requests.post should be called with them and send a message
        # to us from behalf an e-mail address that specified
        send_email(
            name='test',
            email='tester@test.com',
            subject='Test',
            message='Test message.'
        )
        assert mock_post.mock_calls == calls


@mock.patch('app.utils.requests.get')
def test_send_message_to_channel(mock_get, app):
    # Given: attrs for an function.
    calls = [
        mock.call(
            params={
                'chat_id': '12345678', 'text': 'Testing.', 'parse_mode': 'html'
            },
            url='https://api.telegram.org/bot/sendMessage'
        ),
        mock.call().json()
    ]

    # When: the attrs passed to the function.
    with app.app_context():
        # Then: requests.get should be called with them and send HTTP GET to
        # Telegram API which sends a notification to our channel.
        send_message_to_channel(cid='12345678', text='Testing.')
        assert mock_get.mock_calls == calls


@mock.patch('app.utils.requests.post')
def test_send_invoice(mock_post, app):
    # Given: attrs for an function.
    # When: the attrs passed to the function.
    with app.app_context():
        # Then: requests.post should be called with them and send HTTP POST
        # to Mailgun API which sends a e-mail to a client.
        send_invoice(
            email='tester@test.com', message='Testing', subject='Test sbj.'
        )
        assert mock_post.called_once
