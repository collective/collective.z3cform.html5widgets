#python
from datetime import datetime

#zope
from zope import schema
from zope import interface
from zope import component
from zope.schema.fieldproperty import FieldProperty
import z3c.form.browser.widget
import z3c.form.widget
from z3c.form.converter import BaseDataConverter

#plone
import plone.app.z3cform

#internal
from collective.z3cform.html5widgets import attributes

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


class IDateTimeWidget(attributes.IMinMaxWidget,
                      attributes.IRequiredWidget):
    """ Date widget marker for z3c.form """


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
    required_attr = FieldProperty(IDateTimeWidget['required_attr'])

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


class DateTimeConverter(BaseDataConverter):

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return ''
        return value.strftime('%Y-%m-%d-T%H:%MZ')

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        value_length = len(value)
        if value_length == 17:
            #2012-01-26-T13:37
            pattern = '%Y-%m-%d-T%H:%M'
        elif value_length == 18:
            #2012-01-26-T13:37Z
            pattern = '%Y-%m-%d-T%H:%MZ'
        elif value_length == 20:
            #2012-01-26-T13:37:01
            pattern = '%Y-%m-%d-T%H:%M:%S'
        elif value_length == 21:
            #2012-01-26-T13:37:01Z
            pattern = '%Y-%m-%d-T%H:%M:%SZ'
        elif len(value) == 23:
            #2012-01-26-T13:37:01.00
            pattern = '%Y-%m-%d-T%H:%M:%S.00'
        elif len(value) == 24:
            #2012-01-26-T13:37:01.00Z
            pattern = '%Y-%m-%d-T%H:%M:%S.00Z'
        else:
            raise self.raise_error()
        try:
            return datetime.strptime(value, pattern)
        except ValueError:
            self.raise_error()

    def raise_error(self):
        raise DateTimeValidationError
