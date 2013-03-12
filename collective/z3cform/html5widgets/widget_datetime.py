#-*- coding: utf-8 -*-

from datetime import datetime
from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
#from zope.i18n.format import DateTimeParseError
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter


#rfc 3339
#full-date       = date-fullyear "-" date-month "-" date-mday
# returned values
# IE9: display input type text
# Opera: Supported -> 2012-01-26-T13:37:01.00Z
# Safari: Supported -> 2012-01-26-T13:37Z
# IPhone: Supported -> 2012-01-26-T13:37:01Z
# Chrome: input type text
# Chrome mobile (android): supported
# Firefox: display input type text.
# Firefox mobile (android): display input type text with numeric keyboard
# Androidi browser (3.1+): input type text

FORMAT = '%Y-%m-%d-T%H:%MZ'


class IDateTimeWidget(z3c.form.interfaces.IWidget):
    """ Date widget marker for z3c.form """
    min = schema.Date(title=u"Min", required=False)
    max = schema.Date(title=u"Max", required=False)


class IDateTimeField(schema.interfaces.IDatetime):
    """ Special marker for date fields that use our widget """


class DateTimeWidget(z3c.form.browser.widget.HTMLTextInputWidget,
                 z3c.form.widget.Widget):
    """HTML Datetime widget:
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

    interface.implementsOnly(IDateTimeWidget)

    calendar_type = 'gregorian'
    klass = u'html5-datetime-widget'
    min = FieldProperty(IDateTimeWidget['min'])
    max = FieldProperty(IDateTimeWidget['max'])

    def update(self):
        super(DateTimeWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


@component.adapter(schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@interface.implementer(z3c.form.interfaces.IFieldWidget)
def DateTimeFieldWidget(field, request):
    """IFieldWidget factory for DateTimeWidget."""
    return z3c.form.widget.FieldWidget(field, DateTimeWidget(request))


class DateTimeValidationError(schema.ValidationError, ValueError):
    __doc__ = u'Please enter a valid datetime.'


class Converter(BaseDataConverter):

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return ''
        return value.strftime(FORMAT)

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value

        try:
            return datetime.strptime(value, FORMAT)
        except ValueError:
            raise DateTimeValidationError
