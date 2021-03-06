#python
from datetime import datetime

#zope
from zope import schema
from zope import interface
import z3c.form.browser.widget
import z3c.form.widget
from z3c.form.converter import BaseDataConverter
from zope.i18nmessageid.message import MessageFactory

#plone
from plone.app.z3cform.widget import IDateField as pazd
from plone.formwidget.datetime.z3cform.interfaces import IDateField as pfd

#internal
from collective.z3cform.html5widgets import base

#rfc 3339
#full-date       = date-fullyear "-" date-month "-" date-mday
FORMAT = '%Y-%m-%d'
_ = MessageFactory("collective.z3cform.html5widgets")


class IDateWidget(base.IHTML5InputWidget, z3c.form.interfaces.IWidget):
    """Date widget marker for z3c.form """


class IDateField(pazd, pfd):
    pass


class DateWidget(base.HTML5InputWidget, z3c.form.widget.Widget):
    """widget"""

    interface.implementsOnly(IDateWidget)

    klass = u'html5-date-widget'
    input_type = "date"

    def update(self):
        super(DateWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def DateFieldWidget(field, request):
    """IFieldWidget factory for DateWidget."""
    return z3c.form.widget.FieldWidget(field, DateWidget(request))


class DateValidationError(schema.ValidationError, ValueError):
    __doc__ = _(u"Please enter a valid date: 2013-12-28.")


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
