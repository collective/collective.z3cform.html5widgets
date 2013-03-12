#-*- coding: utf-8 -*-

from datetime import datetime
from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
#from zope.i18n.format import DateTimeLocalParseError
from zope.schema.fieldproperty import FieldProperty
from collective.z3cform.html5widgets.widget_datetime import DateTimeConverter
from collective.z3cform.html5widgets import attributes


class IDateTimeLocalWidget(attributes.IMinMaxWidget,
                           attributes.IRequiredWidget):
    """ Date widget marker for z3c.form
    #rfc 3339
    #full-date       = date-fullyear "-" date-month "-" date-mday
    supported:
    # IE9: display input type text
    # Opera: Supported -> 2012-01-26-T13:37:01.00Z
    # Safari: Supported -> 2012-01-26-T13:37Z
    # IPhone: Supported -> 2012-01-26-T13:37:01Z
    # Chrome: input type text
    # Chrome mobile (android): supported
    # Firefox: display input type text.
    # Firefox mobile (android): display input type text with numeric keyboard
    # Androidi browser (3.1+): input type text
    """


class IDateTimeLocalField(schema.interfaces.IDatetime):
    """ Special marker for date fields that use our widget """


class DateTimeLocalWidget(z3c.form.browser.widget.HTMLTextInputWidget,
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

    interface.implementsOnly(IDateTimeLocalWidget)

    calendar_type = 'gregorian'
    klass = u'html5-datetime-widget'
    min = FieldProperty(IDateTimeLocalWidget['min'])
    max = FieldProperty(IDateTimeLocalWidget['max'])
    required_attr = FieldProperty(IDateTimeLocalWidget['required_attr'])

    def update(self):
        super(DateTimeLocalWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


@component.adapter(schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@interface.implementer(z3c.form.interfaces.IFieldWidget)
def DateTimeLocalFieldWidget(field, request):
    """IFieldWidget factory for DateTimeLocalWidget."""
    return z3c.form.widget.FieldWidget(field, DateTimeLocalWidget(request))


class DateTimeLocalValidationError(schema.ValidationError, ValueError):
    __doc__ = u'Please enter a valid datetime.'


class DateTimeLocalConverter(DateTimeConverter):
    def raise_error(self):
        raise DateTimeLocalValidationError
