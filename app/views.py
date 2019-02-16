from copy import deepcopy

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    url_for
)
from jinja2.filters import escape

from app.forms import ContactForm, SubscriptionForm
from app.models import Order
from app.utils import send_email, send_message_to_channel
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

        msg = (
            'Замовлення <b>№{}</b>.\n'
            'Клієнт <b>{}</b> з міста <b>{}</b> замовив підписку <b>{}</b> '
            'у відділення "Нової Пошти" <b>{}</b>.\n'
            'Email: <a href="mailto:{email}">{email}</a>\n'
            'Телефон: <a href="tel:{tel}">{tel}</a>\n'
            'Побажання: <b>{}</b>'
        ).format(
            order.id,
            str(escape(order_data['name'].strip())),
            str(escape(order_data['city'].strip())),
            str(escape(order_data['subscription_type'].strip())),
            str(escape(order_data['department'].strip())),
            str(escape(order_data.get('preferences', 'Немає').strip())),
            email=str(escape(order_data['email'].strip())),
            tel=str(escape(order_data['phone'].strip()))
        )
        send_message_to_channel(
            current_app.config['CHANNEL_ID'],
            msg
        )

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

    if form.validate_on_submit():
        send_email(
            str(escape(form.name.data.strip())),
            str(escape(form.email.data.strip())),
            str(escape(form.subject.data.strip())),
            str(escape(form.message.data.strip()))
        )

        return redirect(url_for('app.email_success'))

    return render_template('app/contacts.html', form=form)


@app_bp.route('/success/')
def success():
    return render_template('app/success.html')


@app_bp.route('/email-success/')
def email_success():
    return render_template('app/email_success.html')


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
