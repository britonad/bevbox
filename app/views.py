import time
import secrets
from app.forms import ContactForm, SubscriptionForm
from app.utils import generate_merchant_signature, get_wayforpay_lang_type
from flask import Blueprint, current_app, render_template, request

app_bp = Blueprint('app', __name__)


@app_bp.route('/')
def home():
    return render_template('app/home.html')


@app_bp.route('/subscription/', methods=['GET', 'POST'])
def subscription():
    context = {}
    subscription_type = request.args.get('type', 'middle')

    form = SubscriptionForm(request.form)

    # Set subscriptions names & values map.
    subscriptions_map = dict(form.subscription_type.choices)
    price = '1' #get_price(form.subscription_type.default.strip())
    context.update(
        {
            'merchantAccount': current_app.config['MERCHANT_LOGIN'],
            'merchantDomainName': 'bevbox.com.ua',
            'orderReference': secrets.token_hex(),
            'orderDate': str(int(time.time())),
            'amount': price,
            'currency': 'UAH',
            'productName': subscriptions_map[form.subscription_type.default],
            'productCount': '1',
            'productPrice': price
        }
    )

    # Creates a merchant signature based on the context above.
    context.update(
        {
            'merchantSignature': generate_merchant_signature(
                list(context.values())
            )
        }
    )

    # Add additional fields that needed for WayForPay, but not include
    # them into creation of a merchant signature.
    context.update(
        {
            'merchantTransactionSecureType': 'AUTO',
            'language': get_wayforpay_lang_type()
        }
    )

    if form.is_submitted():
        if form.validate():
            pass
        else:
            print('error')
            print(form.data)
            print(form.errors)

    return render_template(
        'app/subscription.html',
        form=form,
        context=context,
        subscription_type=subscription_type
    )


@app_bp.route('/contacts/', methods=['GET', 'POST'])
def contacts():
    form = ContactForm(request.form)
    if form.is_submitted():
        if form.validate():
            print('Validate on submit')
            print(form.data)
        else:
            print('on error')
            print(form.data)
            print(form.errors)

    return render_template('app/contacts.html', form=form)


@app_bp.route('/success/')
def success():
    return render_template('app/success.html')


@app_bp.route('/error/')
def error():
    return render_template('app/error.html')


@app_bp.route('/404/')
def not_found():
    return render_template('404.html')


@app_bp.route('/maintenance/')
def maintenance():
    return render_template('app/maintenance.html')


@app_bp.route('/privacy-policy/')
def privacy_policy():
    return render_template('app/privacy-policy.html')


@app_bp.route('/terms-of-use/')
def terms_of_use():
    return render_template('app/terms-of-use.html')


@app_bp.route('/refund-policy/')
def refund_policy():
    return render_template('app/refund-policy.html')
