#python
from datetime import datetime
import pytz

#zope
from zope import schema
from zope import interface
import z3c.form.browser.widget
import z3c.form.widget
from z3c.form.converter import BaseDataConverter
from zope.i18nmessageid.message import MessageFactory

#plone
from plone.app.z3cform import widget

#internal
from collective.z3cform.html5widgets import base

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
_ = MessageFactory("collective.z3cform.html5widgets")
utc = pytz.UTC


class IDateTimeWidget(base.IHTML5InputWidget, z3c.form.interfaces.IWidget):
    """ Date widget marker for z3c.form """


class IDateTimeField(widget.IDatetimeField):
    """ Special marker for date fields that use our widget """


class DateTimeWidget(base.HTML5InputWidget, z3c.form.widget.Widget):
    """widget"""
    interface.implementsOnly(IDateTimeWidget)

    klass = u'html5-datetime-widget'
    input_type = "datetime"

    def update(self):
        super(DateTimeWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def DateTimeFieldWidget(field, request):
    """IFieldWidget factory for DateTimeWidget."""
    return z3c.form.widget.FieldWidget(field, DateTimeWidget(request))


class DateTimeValidationError(schema.ValidationError, ValueError):
    __doc__ = _(u"Please enter a valid datetime: 2013-12-28-T23:59Z.")


class DateTimeConverter(BaseDataConverter):

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return ''
        return value.strftime('%Y-%m-%dT%H:%MZ')

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value

        pattern = self.getDatePattern(value)

        try:
            return utc.localize(datetime.strptime(value, pattern))
        except ValueError:
            self.raise_error()

    def getDatePattern(self, value):
        value_length = len(value)

        if value_length == 16:
            #2013-08-01T01:01
            pattern = '%Y-%m-%dT%H:%M'
        elif value_length == 17:
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
        return pattern

    def raise_error(self):
        raise DateTimeValidationError
