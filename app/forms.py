from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms.fields import RadioField, StringField, TextAreaField
from wtforms.validators import Email, Length, DataRequired


class BaseForm(FlaskForm):
    """
    A base form representation.
    """

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
    """
    A representation of a contact form.
    """

    message = TextAreaField(
        label=_('Message'),
        validators=[DataRequired(), Length(max=4096)],
        render_kw={'placeholder': '...'}
    )


class SubscriptionForm(BaseForm):
    """
    A representation of a subscription form.
    """

    phone = StringField(
        label=_('Phone'),
        validators=[DataRequired(), Length(max=15)],
        render_kw={'placeholder': '+380123456789', 'type': 'tel'},
    )
    subscription_type = RadioField(
        label=_('Subscription type'),
        default='middle',
        choices=[
            ('junior', _('Junior 1 month / ₴ 1373')),
            (
                'middle',
                _(
                    'Middle 2 months / ₴ 2608 (you save 5%(percent)s)',
                    percent='%'
                )
            ),
            (
                'senior',
                _(
                    'Senior 3 months / ₴ 3707 (you save 10%(percent)s)',
                    percent='%'
                )
            )
        ]
    )
    city = StringField(
        label=_('City'),
        validators=[DataRequired(), Length(max=256)],
        render_kw={'placeholder': _('Kyiv')}
    )
    department = StringField(
        label=_('Department of New Post (NovaPoshta)'),
        validators=[DataRequired(), Length(max=5)],
        render_kw={'placeholder': 1}
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
