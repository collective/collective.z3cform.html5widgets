#-*- coding: utf-8 -*-

from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
#from zope.i18n.format import TelTimeParseError
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets import attributes


PATTERN = "((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,5})|(\(?\d{2,6}\)?))(-| )?"
PATTERN += "(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$"


class ITelWidget(attributes.IPatternWidget,
                 attributes.IRequiredWidget):
    """ Tel widget marker for z3c.form """


class ITelField(schema.interfaces.IASCIILine):
    """ Special marker for date fields that use our widget """


class TelWidget(z3c.form.browser.widget.HTMLTextInputWidget,
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

    interface.implementsOnly(ITelWidget)

    klass = u'html5-tel-widget'
    pattern = FieldProperty(ITelWidget['pattern'])
    required_attr = FieldProperty(ITelWidget['required_attr'])

    def update(self):
        super(TelWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def TelFieldWidget(field, request):
    """IFieldWidget factory for TelWidget."""
    return z3c.form.widget.FieldWidget(field, TelWidget(request))


class TelValidationError(schema.ValidationError, ValueError):
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
            raise TelValidationError
