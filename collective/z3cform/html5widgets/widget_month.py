#-*- coding: utf-8 -*-

from datetime import datetime
from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter

from collective.z3cform.html5widgets import base
from zope.i18nmessageid.message import MessageFactory

#rfc 3339
#full-date       = date-fullyear "-" date-month "-" date-mday
FORMAT = '%Y-%m'
_ = MessageFactory("collective.z3cform.html5widgets")


class IMonthWidget(base.IHTML5InputWidget, z3c.form.interfaces.IWidget):
    """Date widget marker for z3c.form """


class IMonthField(schema.interfaces.IDate):
    """ Special marker for date fields that use our widget """


class MonthWidget(base.HTML5InputWidget, z3c.form.widget.Widget):
    """Widget"""

    interface.implementsOnly(IMonthWidget)

    klass = u'html5-month-widget'
    input_type = "month"

    def update(self):
        super(MonthWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def MonthFieldWidget(field, request):
    """IFieldWidget factory for MonthWidget."""
    return z3c.form.widget.FieldWidget(field, MonthWidget(request))


class MonthValidationError(schema.ValidationError, ValueError):
    __doc__ = _(u"Please enter a valid month: 2013-12.")


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
