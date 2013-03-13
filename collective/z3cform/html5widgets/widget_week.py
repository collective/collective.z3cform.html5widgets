#-*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter

from collective.z3cform.html5widgets import attributes


class IWeekWidget(attributes.IStepWidget,
                  attributes.IMinMaxWidget,
                  attributes.IRequiredWidget):
    """Week widget marker for z3c.form """


class IWeekField(schema.interfaces.IDate):
    """ Special marker for date fields that use our widget """


class WeekWidget(z3c.form.browser.widget.HTMLTextInputWidget,
                 z3c.form.widget.Widget):
    """HTML Week widget:
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

    interface.implementsOnly(IWeekWidget)

    klass = u'html5-date-widget'
    step = FieldProperty(IWeekWidget['step'])
    min = FieldProperty(IWeekWidget['min'])
    max = FieldProperty(IWeekWidget['max'])
    required_attr = FieldProperty(IWeekWidget['required_attr'])

    def update(self):
        super(WeekWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def WeekFieldWidget(field, request):
    """IFieldWidget factory for WeekWidget."""
    return z3c.form.widget.FieldWidget(field, WeekWidget(request))


class WeekValidationError(schema.ValidationError, ValueError):
    __doc__ = u'Please enter a valid date.'


class Converter(BaseDataConverter):

    def tofirstdayinisoweek(self, year, week):
        ret = datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
        if date(year, 1, 4).isoweekday() > 4:
            ret -= timedelta(days=7)
        return ret.date()

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return ''
        return '%02d-W%02d' % (value.year, value.isocalendar()[1])

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        value_length = len(value)
        if value_length == 8:
            year = int(value[:4])
            week = int(value[-2:])
        try:
            return self.tofirstdayinisoweek(year, week)
        except ValueError:
            raise WeekValidationError
