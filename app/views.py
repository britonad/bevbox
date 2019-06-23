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
from app.utils import (
    create_invoice_msg,
    create_order_notification_msg,
    send_email,
    send_invoice,
    send_message_to_channel,
)
from core import db

app_bp = Blueprint('app', __name__)


@app_bp.route('/')
def home():
    return render_template('app/home.html')


@app_bp.route('/subscription/', methods=['GET', 'POST'])
def subscription():
    subscription_type = request.args.get('type', SubscriptionForm.JUNIOR)
    form = SubscriptionForm(request.form)
    form.subscription_type.data = subscription_type

    if form.validate_on_submit():
        order_data = deepcopy(form.data)
        order_data.pop('csrf_token')

        # Save to a DB order info.
        order = Order(**order_data)
        db.session.add(order)
        db.session.commit()

        # Notify about an order.
        send_message_to_channel(
            cid=current_app.config['CHANNEL_ID'],
            text=create_order_notification_msg(order, order_data)
        )

        # Send an invoice to a customer in case of choosing credit card
        # payment option.
        if order_data['payment_option'] == SubscriptionForm.CREDIT_CARD:
            send_invoice(
                email=str(escape(order_data['email'].strip())),
                message=create_invoice_msg(order_data),
                subject='Bevbox Invoice'
            )

        return redirect(url_for('app.success'))

    return render_template(
        'app/subscription.html',
        form=form,
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
