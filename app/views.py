from flask import Blueprint, render_template

app_bp = Blueprint('app', __name__)


@app_bp.route('/')
def home():
    return render_template('app/home.html')


@app_bp.route('/subscription/', methods=['GET', 'POST'])
def subscription():
    return render_template('app/subscription.html')


@app_bp.route('/contacts/', methods=['GET', 'POST'])
def contacts():
    return render_template('app/contacts.html')


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
