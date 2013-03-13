#-*- coding: utf-8 -*-

from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
#from zope.i18n.format import PasswordTimeParseError
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets import attributes


class IPasswordWidget(attributes.IPatternWidget,
                 attributes.IRequiredWidget):
    """ Password widget marker for z3c.form """


class IPasswordField(schema.interfaces.IPassword):
    """ Special marker for date fields that use our widget """


class PasswordWidget(z3c.form.browser.widget.HTMLTextInputWidget,
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

    interface.implementsOnly(IPasswordWidget)

    klass = u'html5-password-widget'
    pattern = FieldProperty(IPasswordWidget['pattern'])
    required_attr = FieldProperty(IPasswordWidget['required_attr'])

    def update(self):
        super(PasswordWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def PasswordFieldWidget(field, request):
    """IFieldWidget factory for PasswordWidget."""
    return z3c.form.widget.FieldWidget(field, PasswordWidget(request))


class PasswordValidationError(schema.ValidationError, ValueError):
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
            return value
        except ValueError:
            raise PasswordValidationError
