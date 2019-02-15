from copy import deepcopy

from flask import Blueprint, redirect, render_template, request, url_for

from app.forms import ContactForm, SubscriptionForm
from app.models import Order
from core import db

app_bp = Blueprint('app', __name__)


@app_bp.route('/')
def home():
    return render_template('app/home.html')


@app_bp.route('/subscription/', methods=['GET', 'POST'])
def subscription():
    context = {}
    subscription_type = request.args.get('type', 'middle')

    form = SubscriptionForm(request.form)

    if form.validate_on_submit():
        order_data = deepcopy(form.data)
        order_data.pop('csrf_token')

        order = Order(**order_data)
        db.session.add(order)
        db.session.commit()

        return redirect(url_for('app.success'))

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
