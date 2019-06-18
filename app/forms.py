from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms.fields import (
    BooleanField,
    IntegerField,
    RadioField,
    StringField,
    TextAreaField
)
from wtforms.validators import DataRequired, Email, Length


class BaseForm(FlaskForm):
    """A base form representation."""

    email = StringField(
        label=_('E-mail'),
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'root@ukr.net', 'type': 'email'},
    )
    name = StringField(
        label=_('Name'),
        validators=[DataRequired(), Length(min=4, max=256)],
        render_kw={'placeholder': _('John Doe')}
    )


class ContactForm(BaseForm):
    """A representation of a contact form."""

    subject = StringField(
        label=_('Subject'),
        validators=[DataRequired(), Length(min=4, max=256)],
        render_kw={'placeholder': _('A subject.')}
    )
    message = TextAreaField(
        label=_('Message'),
        validators=[DataRequired(), Length(max=4096)],
        render_kw={'placeholder': '...'}
    )


class SubscriptionForm(BaseForm):
    """A representation of a subscription form."""

    # Payment options values.
    CREDIT_CARD = 'cc'
    IMPOSED_PAYMENT = 'ip'
    # Subscriptions options values.
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'

    phone = StringField(
        label=_('Phone'),
        validators=[DataRequired(), Length(max=15)],
        render_kw={'placeholder': '+380123456789', 'type': 'tel'},
    )
    subscription_type = RadioField(
        label=_('Subscription type'),
        default='middle',
        choices=(
            (JUNIOR, _('Junior 1 month / ₴ 2391')),
            (
                MIDDLE,
                _(
                    'Middle 2 months / ₴ 4542 (you save 5%(percent)s)',
                    percent='%'
                )
            ),
            (
                SENIOR,
                _(
                    'Senior 3 months / ₴ 6455 (you save 10%(percent)s)',
                    percent='%'
                )
            )
        )
    )
    payment_option = RadioField(
        label=_('Payment option'),
        default=CREDIT_CARD,
        choices=(
            (CREDIT_CARD, _('Credit Card Prepayment')),
            (IMPOSED_PAYMENT, _('Imposed Payment'))
        )
    )
    city = StringField(
        label=_('City'),
        validators=[DataRequired(), Length(max=256)],
        render_kw={'placeholder': _('Kyiv')}
    )
    department = IntegerField(
        label=_('Department of New Post (NovaPoshta)'),
        validators=[DataRequired()],
        render_kw={'placeholder': 1}
    )
    # delivery_option = RadioField(
    #     label=_('Delivery option'),
    #     default='ww',
    #     choices=(
    #         ('ww', _('Warehouse-Warehouse')),
    #         ('wa', _('Warehouse-Address'))
    #     )
    # )
    # delivery_address = StringField(
    #     label=_('Delivery Address'),
    #     validators=[Length(max=256)],
    #     render_kw={'placeholder': _('Verkhniy Val, 31')},
    #     description=_(
    #         'You can omit this field if you chose delivery option '
    #         'Warehouse-Warehouse.'
    #     )
    # )
    matches = BooleanField(
        label=_('Matches'),
        default=True,
        render_kw={},
        description=_('Not include matches? - ₴50')
    )
    stones = BooleanField(
        label=_('Stones'),
        default=True,
        render_kw={},
        description=_('Not include stones? - ₴200')
    )
    guillotine = BooleanField(
        label=_('Guillotine'),
        default=True,
        render_kw={},
        description=_('Not include guillotine? - ₴80')
    )
    preferences = TextAreaField(
        label=_('Preferences'),
        validators=[Length(max=2048)],
        render_kw={
            'placeholder': _(
                'I like a single malt whiskey etc. Leave blank if doesnt '
                'have one.'
            )
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: Follow SOLID.
        # Set checked attr.
        checked = {'checked': 'checked'}
        if self.is_submitted():
            if self.matches.data:
                self.matches.render_kw = checked

            if self.stones.data:
                self.stones.render_kw = checked

            if self.guillotine.data:
                self.guillotine.render_kw = checked

            if not self.callback.data:
                self.callback.render_kw = {}

    # def validate_delivery_address(self, field):
    #     # TODO: Fix hardcode.
    #     if not field.data and self.delivery_option.data == 'wa':
    #         raise ValidationError(
    #             _(
    #                 'Delivery address should be set when delivery option is '
    #                 'Warehouse-Address.'
    #             )
    #         )

