import requests
from flask import current_app, render_template
from flask_babel import lazy_gettext as _
from jinja2.filters import escape

from app.forms import SubscriptionForm
from app.models import Order


def get_price(subscription_type: str) -> int:
    """Gets a price of a subscription by a provided subscription type."""

    prices = {
        SubscriptionForm.JUNIOR: 2391,
        SubscriptionForm.MIDDLE: 4542,
        SubscriptionForm.SENIOR: 6455
    }

    return prices.get(subscription_type, 0)


def get_subscription_name(subscription_type: str) -> str:
    """Gets a subscription l10n name by a provided subscription type."""

    subscriptions_names = {
        SubscriptionForm.JUNIOR: _('Junior'),
        SubscriptionForm.MIDDLE: _('Middle'),
        SubscriptionForm.SENIOR: _('Senior')
    }

    return subscriptions_names.get(subscription_type)


def calculate_subscription_cost(order_data: dict) -> int:
    """Calculates cost of subscription that relies on additions."""

    # TODO: Decouple functionality.
    subscription_price = get_price(order_data['subscription_type'])
    cigar = 500 if order_data['cigar'] else 0
    matches = 50 if order_data['matches'] else 0
    guillotine = 80 if order_data['guillotine'] else 0
    stones = 200 if order_data['stones'] else 0
    reduced_goods_price = cigar + matches + guillotine + stones

    if order_data['subscription_type'] == SubscriptionForm.SENIOR:
        reduced_goods_price *= 3
    elif order_data['subscription_type'] == SubscriptionForm.MIDDLE:
        reduced_goods_price *= 2

    return subscription_price - reduced_goods_price


def create_invoice_msg(order_data: dict) -> str:
    """Creates a message for an invoice based on a template."""

    cost = calculate_subscription_cost(order_data)

    return render_template(
        'invoice/invoice_msg.html',
        cost=cost,
        credit_card=current_app.config['CREDIT_CARD'],
        name=str(escape(order_data['name'].strip())),
        subscription_type=get_subscription_name(
            order_data['subscription_type']
        )
    )


def create_order_notification_msg(order: Order, order_data: dict) -> str:
    """Creates a Telegram notification message from subscription form data."""

    # TODO: Move to a template.
    msg = (
        'Замовлення <b>№{}</b>.\n'
        'Клієнт <b>{}</b> з міста <b>{}</b> замовив підписку <b>{}</b> '
        'у відділення "Нової Пошти" <b>№{}</b>.\n'
        'Email: <a href="mailto:{email}">{email}</a>\n'
        'Телефон: <a href="tel:{tel}">{tel}</a>\n'
        'Варіант оплати: <b>{}</b>\n'
        # 'Варіант доставки: <b>{}</b>\n'
        # 'Адресса доставки: <b>{}</b>\n'
        'Сигара: <b>{}</b>\n'
        'Сірники: <b>{}</b>\n'
        'Каміньці: <b>{}</b>\n'
        'Гільйотина: <b>{}</b>\n'
        'Побажання: <b>{}</b>\n'
        '\n'
        '<b>Вартість</b>: <i>₴{}</i>'
    ).format(
        order.id,
        str(escape(order_data['name'].strip())),
        str(escape(order_data['city'].strip())),
        str(escape(order_data['subscription_type'].strip())),
        str(escape(order_data['department'])),
        str(escape(order_data['payment_option'])),
        # str(escape(order_data['delivery_option'])),
        # str(escape(order_data.get('delivery_address', '-').strip())),
        'ні' if order_data['cigar'] else 'так',
        'ні' if order_data['matches'] else 'так',
        'ні' if order_data['stones'] else 'так',
        'ні' if order_data['guillotine'] else 'так',
        str(
            escape(
                order_data['preferences']
                if order_data['preferences'] else 'Немає'
            ).strip()
        ),
        calculate_subscription_cost(order_data),
        email=str(escape(order_data['email'].strip())),
        tel=str(escape(order_data['phone'].strip()))
    )

    return msg


def send_email(
        name: str,
        email: str,
        subject: str,
        message: str
) -> str:
    """Sends an e-mail by means of external call of Mailgun API to a recipient
    from a predefined settings behalf of a sender.
    """

    return requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(
            current_app.config['MAILGUN_DOMAIN_NAME']
        ),
        auth=('api', current_app.config['MAILGUN_API_KEY']),
        data={
            'from': '{} <{}>'.format(name, email),
            'to': current_app.config['EMAIL_RECIPIENT'],
            'subject': subject,
            'text': message
        }
    ).text


def send_message_to_channel(cid: str, text: str) -> dict:
    """Sends a message by provided a text argument to a specified Telegram
    channel.
    """

    api_url = '{}/bot{}/sendMessage'.format(
        current_app.config['TELEGRAM_API_URL'],
        current_app.config['BOT_TOKEN']
    )

    return requests.get(
        url=api_url,
        params={
            'chat_id': cid,
            'text': text,
            'parse_mode': 'html'
        }
    ).json()


def send_invoice(
        email: str, message: str, subject: str, **kwargs
) -> str:
    """Send a message to users that subscribed to a mailing list."""

    response = requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(
            current_app.config['MAILGUN_DOMAIN_NAME']
        ),
        auth=('api', current_app.config['MAILGUN_API_KEY']),
        data={
            'from': 'Bevbox Company <{}>'.format(
                current_app.config['EMAIL_RECIPIENT']
            ),
            'to': email,
            'subject': subject,
            'html': render_template(
                'invoice/email_template.html',
                subject=subject,
                message=message,
                **kwargs
            )
        }
    ).text

    return response
