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
FORMAT = '%Y-%m-%d'


class IDateWidget(z3c.form.interfaces.IWidget):
    """ Date widget marker for z3c.form """
    step = schema.Int(title=u"Step", required=False)
    min = schema.Date(title=u"Min", required=False)
    max = schema.Date(title=u"Max", required=False)


class IDateField(schema.interfaces.IDate):
    """ Special marker for date fields that use our widget """


class DateWidget(z3c.form.browser.widget.HTMLTextInputWidget,
                 z3c.form.widget.Widget):
    """HTML Date widget:
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

    interface.implementsOnly(IDateWidget)

    calendar_type = 'gregorian'
    klass = u'html5-date-widget'
    step = FieldProperty(IDateWidget['step'])
    min = FieldProperty(IDateWidget['min'])
    max = FieldProperty(IDateWidget['max'])

    def update(self):
        super(DateWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)

#    @property
#    def date(self):
#        date = self.request.get(self.name, None)
#        if date is not None:
#            return date
#        return self.value


@component.adapter(schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@interface.implementer(z3c.form.interfaces.IFieldWidget)
def DateFieldWidget(field, request):
    """IFieldWidget factory for DateWidget."""
    return z3c.form.widget.FieldWidget(field, DateWidget(request))


class DateValidationError(schema.ValidationError, ValueError):
    __doc__ = u'Please enter a valid date.'


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
            raise DateValidationError
