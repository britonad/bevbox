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
    city = db.Column(db.String(256), nullable=False)
    department = db.Column(db.Integer, nullable=False)
    preferences = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Order {}-{}>'.format(self.email, self.id)
