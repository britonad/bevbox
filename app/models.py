from core import db


class Order(db.Model):
    """
    Order model representation. It basically interacts with a subscription
    form.
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    subscription_type = db.Column(db.String(10), nullable=False)
    payment_option = db.Column(db.String(2), nullable=True)
    city = db.Column(db.String(256), nullable=False)
    department = db.Column(db.Integer, nullable=False)
    # delivery_option = db.Column(db.String(2), nullable=False)
    # delivery_address = db.Column(db.String(256), nullable=True)
    matches = db.Column(db.Boolean, nullable=True)
    stones = db.Column(db.Boolean, nullable=True)
    guillotine = db.Column(db.Boolean, nullable=True)
    preferences = db.Column(db.Text, nullable=True)
    callback = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return '<Order {}-{}>'.format(self.email, self.id)
