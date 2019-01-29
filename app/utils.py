import hmac

from flask import current_app, g


def get_price(value: str) -> str:
    """
    Gets a price from a map by provided value.
    """

    prices_map = {
        'junior': '1373',
        'middle': '2608',
        'senior': '3707'
    }

    return prices_map[value]


def get_wayforpay_lang_type() -> str:
    """
    Gets a language of a user session and picks from a map corresponding value
    for WayForPay.
    """

    languages_map = {
        'uk': 'UA',
        'ru': 'RU',
        'en': 'EN'
    }
    if g.lang:
        return languages_map.get(g.lang, 'UA')
    else:
        return 'UA'


def transform_to_flat_list(data: list) -> list:
    """
    Transforms a two-dimensional list that consists of ints, strings, lists to
    one-dimensional.
    """

    new = []

    # TODO: Think about a better implementation that can take n-dimensions.
    for index in data:
        if isinstance(index, list):
            for element in index:
                new.append(str(element))
        else:
            new.append(str(index))

    return new


def generate_merchant_signature(data: list) -> str:
    """
    For the purposes of confirmation of data validity, there should be
    generated and transferred in the request the HMAC_MD5 control signature
    using SecretKey of a merchant.

    The line which subjects to HMAC_MD5 is generated through concatenation of
    parameters merchantAccount, merchantDomainName, orderReference, orderDate,
    amount, currency, productName[0], productName[1]..., productName[n],
    productCount[0], productCount[1],..., productCount[n], productPrice[0],
    productPrice[1],..., productPrice[n]  divided with “;” (semi-column) in
    coding UTF-8.
    """

    app = current_app._get_current_object()
    value = ';'.join(transform_to_flat_list(data))

    return hmac.new(
        app.config['MERCHANT_SECRET_KEY'].encode(),
        value.encode()
    ).hexdigest()
