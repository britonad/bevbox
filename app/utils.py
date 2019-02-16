import requests
from flask import current_app


def send_message_to_channel(cid: str, text: str) -> dict:
    """
    Sends a message provided by a text argument to a specified Telegram channel.
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
