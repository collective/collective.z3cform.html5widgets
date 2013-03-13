#-*- coding: utf-8 -*-

from datetime import datetime
from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter

from collective.z3cform.html5widgets.widget_date import IDateWidget

#rfc 3339
#full-date       = date-fullyear "-" date-month "-" date-mday
FORMAT = '%Y-%m'


class IMonthWidget(IDateWidget):
    """Date widget marker for z3c.form """


class IMonthField(schema.interfaces.IDate):
    """ Special marker for date fields that use our widget """


class MonthWidget(z3c.form.browser.widget.HTMLTextInputWidget,
                 z3c.form.widget.Widget):
    """HTML Month widget:
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
    * step (integer)
    * readonly
    * required
    * value
    * pattern
    """

    interface.implementsOnly(IMonthWidget)

    klass = u'html5-month-widget'
    step = FieldProperty(IMonthWidget['step'])
    min = FieldProperty(IMonthWidget['min'])
    max = FieldProperty(IMonthWidget['max'])
    required_attr = FieldProperty(IMonthWidget['required_attr'])

    def update(self):
        super(MonthWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def MonthFieldWidget(field, request):
    """IFieldWidget factory for MonthWidget."""
    return z3c.form.widget.FieldWidget(field, MonthWidget(request))


class MonthValidationError(schema.ValidationError, ValueError):
    __doc__ = u'Please enter a valid month.'


class Converter(BaseDataConverter):

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return ''
        return value.strftime(FORMAT)

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value

        try:
            return datetime.strptime(value, FORMAT).date()
        except ValueError:
            raise MonthValidationError
