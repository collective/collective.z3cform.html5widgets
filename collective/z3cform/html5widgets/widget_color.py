#-*- coding: utf-8 -*-

from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets import attributes


class IColorWidget(attributes.IRequiredWidget):
    """ Color widget marker for z3c.form
    http://www.w3.org/TR/html-markup/input.color.html
    """


class IColorField(schema.interfaces.IASCIILine):
    """ Special marker for date fields that use our widget """


class ColorWidget(z3c.form.browser.widget.HTMLTextInputWidget,
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

    interface.implementsOnly(IColorWidget)

    klass = u'html5-color-widget'
    required_attr = FieldProperty(IColorWidget['required_attr'])

    def update(self):
        super(ColorWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


@component.adapter(schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@interface.implementer(z3c.form.interfaces.IFieldWidget)
def ColorFieldWidget(field, request):
    """IFieldWidget factory for ColorWidget."""
    return z3c.form.widget.FieldWidget(field, ColorWidget(request))


class ColorValidationError(schema.ValidationError, ValueError):
    __doc__ = u'Please enter a valid color (#0590FF)'


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
            raise ColorValidationError
