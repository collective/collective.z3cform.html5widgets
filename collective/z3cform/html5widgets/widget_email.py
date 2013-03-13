#-*- coding: utf-8 -*-

from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
#from zope.i18n.format import EmailTimeParseError
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets import attributes


class IEmailWidget(attributes.IPatternWidget,
                   attributes.IRequiredWidget,
                   attributes.IPlaceholder):
    """ Email widget marker for z3c.form
    http://www.w3.org/TR/html-markup/input.email.html
    """


class IEmailField(schema.interfaces.IASCIILine):
    """ Special marker for date fields that use our widget """


class EmailWidget(z3c.form.browser.widget.HTMLTextInputWidget,
                z3c.form.widget.Widget):
    """
    browser support:
    * IE 10: OK
    * IE < 10: input type text

    attributes:
    * name
    * disabled
    * form
    * type
    * autocomplete
    * autofocus
    * list
    * min
    * max
    * readonly
    * required
    * value
    * pattern
    """

    interface.implementsOnly(IEmailWidget)

    klass = u'html5-email-widget'
    pattern = FieldProperty(IEmailWidget['pattern'])
    required_attr = FieldProperty(IEmailWidget['required_attr'])
    placeholder = FieldProperty(IEmailWidget['placeholder'])

    def update(self):
        super(EmailWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def EmailFieldWidget(field, request):
    """IFieldWidget factory for EmailWidget."""
    return z3c.form.widget.FieldWidget(field, EmailWidget(request))


class EmailValidationError(schema.ValidationError, ValueError):
    __doc__ = u'Please enter a valid date.'


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
