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
        choices=(
            ('junior', _('Junior 1 month / ₴ 1705')),
            (
                'middle',
                _(
                    'Middle 2 months / ₴ 3239 (you save 5%(percent)s)',
                    percent='%'
                )
            ),
            (
                'senior',
                _(
                    'Senior 3 months / ₴ 4603 (you save 10%(percent)s)',
                    percent='%'
                )
            )
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
    additions = BooleanField(
        label=_('Do you need guillotine & matches as well?'),
        default=True,
        description=_(
            'Uncheck if you do not need it and yes, it reduces the cost of '
            'the box by 129₴. E.g.: Junior will cost 1253₴, Middle 2366₴, '
            'Senior 3347₴.'
        )
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

        # Set checked attr..
        if self.additions.data:
            self.additions.render_kw = {'checked': 'checked'}
        else:
            self.additions.render_kw = {'checked': ''}
