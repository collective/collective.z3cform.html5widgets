#-*- coding: utf-8 -*-
from datetime import datetime

from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
#from zope.i18n.format import TimeTimeParseError
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets import attributes


class ITimeWidget(attributes.IStepWidget,
                  attributes.IMinMaxWidget,
                  attributes.IRequiredWidget):
    """ Time widget marker for z3c.form """


class ITimeField(schema.interfaces.ITime):
    """ Special marker for date fields that use our widget """


class TimeWidget(z3c.form.browser.widget.HTMLTextInputWidget,
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

    interface.implementsOnly(ITimeWidget)

    klass = u'html5-time-widget'
    required_attr = FieldProperty(ITimeWidget['required_attr'])
    step = FieldProperty(ITimeWidget['step'])
    min = FieldProperty(ITimeWidget['min'])
    max = FieldProperty(ITimeWidget['max'])

    def update(self):
        super(TimeWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


@component.adapter(schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@interface.implementer(z3c.form.interfaces.IFieldWidget)
def TimeFieldWidget(field, request):
    """IFieldWidget factory for TimeWidget."""
    return z3c.form.widget.FieldWidget(field, TimeWidget(request))


class TimeValidationError(schema.ValidationError, ValueError):
    __doc__ = u'Please enter a valid date.'


class Converter(BaseDataConverter):

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return ''
        return value.strftime('%H:%M')

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        try:
            return datetime.strptime(value, '%H:%M').time()
        except ValueError:
            raise TimeValidationError
