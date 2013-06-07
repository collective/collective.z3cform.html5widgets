#-*- coding: utf-8 -*-
from datetime import datetime

from zope import schema
from zope import interface
import z3c.form.browser.widget
import z3c.form.widget
#from zope.i18n.format import TimeTimeParseError
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets import base
from zope.i18nmessageid.message import MessageFactory

_ = MessageFactory("collective.z3cform.html5widgets")


class ITimeWidget(base.IHTML5InputWidget, z3c.form.interfaces.IWidget):
    """ Time widget marker for z3c.form """


class ITimeField(schema.interfaces.ITime):
    """ Special marker for date fields that use our widget """


class TimeWidget(base.HTML5InputWidget, z3c.form.widget.Widget):
    """widget"""

    interface.implementsOnly(ITimeWidget)

    klass = u'html5-time-widget'
    input_type = "time"

    def update(self):
        super(TimeWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def TimeFieldWidget(field, request):
    """IFieldWidget factory for TimeWidget."""
    return z3c.form.widget.FieldWidget(field, TimeWidget(request))


class TimeValidationError(schema.ValidationError, ValueError):
    __doc__ = _(u"Please enter a valid time: 23:59.")


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
