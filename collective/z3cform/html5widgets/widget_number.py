#-*- coding: utf-8 -*-

from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets import attributes


class INumberWidget(attributes.IStepWidget,
                    attributes.IMinMaxWidget,
                    attributes.IRequiredWidget):
    """ Number widget marker for z3c.form """


class INumberField(schema.interfaces.IASCIILine):
    """ Special marker for date fields that use our widget """


class NumberWidget(z3c.form.browser.widget.HTMLTextInputWidget,
                z3c.form.widget.Widget):
    """HTML  widget:
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

    interface.implementsOnly(INumberWidget)

    klass = u'html5-number-widget'
    max = FieldProperty(INumberWidget['max'])
    min = FieldProperty(INumberWidget['min'])
    required_attr = FieldProperty(INumberWidget['required_attr'])
    step = FieldProperty(INumberWidget['step'])

    def update(self):
        super(NumberWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


@component.adapter(schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@interface.implementer(z3c.form.interfaces.IFieldWidget)
def NumberFieldWidget(field, request):
    """IFieldWidget factory for NumberWidget."""
    return z3c.form.widget.FieldWidget(field, NumberWidget(request))


class NumberValidationError(schema.ValidationError, ValueError):
    __doc__ = u'Please enter a valid number.'


class Converter(BaseDataConverter):

    def toWidgetValue(self, value):
        return value

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value

        try:
            return value
        except ValueError:
            raise NumberValidationError
