#-*- coding: utf-8 -*-

from zope import schema
from zope import interface
import z3c.form.browser.widget
import z3c.form.widget
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets import base
from zope.i18nmessageid.message import MessageFactory

_ = MessageFactory("collective.z3cform.html5widgets")


class IEmailWidget(base.IHTML5InputWidget, z3c.form.interfaces.IWidget):
    """ Email widget marker for z3c.form
    http://www.w3.org/TR/html-markup/input.email.html
    """


class IEmailField(schema.interfaces.IASCIILine):
    """ Special marker for date fields that use our widget """


class EmailWidget(base.HTML5InputWidget, z3c.form.widget.Widget):
    """widget"""

    interface.implementsOnly(IEmailWidget)

    klass = u'html5-email-widget'
    input_type = "email"

    def update(self):
        super(EmailWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def EmailFieldWidget(field, request):
    """IFieldWidget factory for EmailWidget."""
    return z3c.form.widget.FieldWidget(field, EmailWidget(request))


class EmailValidationError(schema.ValidationError, ValueError):
    __doc__ = _(u"Please enter a valid email: name@domain.com.")


class Converter(BaseDataConverter):

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return ''
        return value

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        try:
            return str(value)
        except UnicodeEncodeError:
            raise EmailValidationError
