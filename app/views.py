import secrets
import requests
from app.forms import ContactForm, SubscriptionForm
from app.utils import generate_merchant_signature
from flask import Blueprint, current_app, g, render_template, request, redirect, render_template_string

app_bp = Blueprint('app', __name__)


@app_bp.route('/')
def home():
    return render_template('app/home.html')


@app_bp.route('/subscription/', methods=['GET', 'POST'])
def subscription():
    query_data = {
        'merchantAccount': current_app.config['MERCHANT_LOGIN'],
        'merchantDomainName': 'bevbox.com.ua',
        'orderReference': secrets.token_hex(),
        'orderDate': '1415379863',
        'amount': '2',
        'currency': 'UAH',
        'productName': ['Bevbox'],
        'productCount': ['1'],
        'productPrice': ['2']
    }
    merchant_signiture = generate_merchant_signature(
        list(query_data.values())
    )

    query_data.update(
        {
            'merchantTransactionSecureType': 'AUTO',
            'merchantSignature': merchant_signiture,
            'language': g.lang if g.lang else 'UA',
        }
    )
    return render_template_string(requests.post(
        'https://secure.wayforpay.com/pay',
        data=query_data
    ).text)
    print(reponse)
    prices = {
        'junior': 1373,
        'middle': 2608,
        'senior': 3707
    }
    subscription_type = request.args.get('type', 'middle')
    form = SubscriptionForm(request.form)
    if form.is_submitted():
        if form.validate():
            print(form.data)
        else:
            print('error')
            print(form.data)
            print(form.errors)

    return render_template(
        'app/subscription.html',
        form=form,
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
