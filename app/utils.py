import requests
from flask import current_app


def send_email(
        name: str,
        email: str,
        subject: str,
        message: str
) -> str:
    """
    Sends an e-mail by means of external call of Mailgun API to a recipient
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
    """
    Sends a message by provided a text argument to a specified Telegram channel.
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
