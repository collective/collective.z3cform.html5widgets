#-*- coding: utf-8 -*-

from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
#from zope.i18n.format import URLTimeParseError
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets import attributes


class IURLWidget(attributes.IPatternWidget,
                 attributes.IRequiredWidget):
    """ URL widget marker for z3c.form """


class IURLField(schema.interfaces.IURI):
    """ Special marker for date fields that use our widget """


class URLWidget(z3c.form.browser.widget.HTMLTextInputWidget,
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

    interface.implementsOnly(IURLWidget)

    klass = u'html5-tel-widget'
    pattern = FieldProperty(IURLWidget['pattern'])
    required_attr = FieldProperty(IURLWidget['required_attr'])

    def update(self):
        super(URLWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


@component.adapter(schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@interface.implementer(z3c.form.interfaces.IFieldWidget)
def URLFieldWidget(field, request):
    """IFieldWidget factory for URLWidget."""
    return z3c.form.widget.FieldWidget(field, URLWidget(request))


class URLValidationError(schema.ValidationError, ValueError):
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
        except ValueError:
            raise URLValidationError
