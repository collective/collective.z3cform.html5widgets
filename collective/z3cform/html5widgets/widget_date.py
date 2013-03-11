#-*- coding: utf-8 -*-

from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
from interfaces import IDateWidget
from zope.i18n.format import DateTimeParseError


class DateWidget(z3c.form.browser.widget.HTMLTextInputWidget,
                 z3c.form.widget.Widget):
    """ Date widget. """

    interface.implementsOnly(IDateWidget)

    calendar_type = 'gregorian'
    klass = u'html5-date-widget'
    value = ('', '', '')

    def update(self):
        super(DateWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)

    @property
    def date(self):
        return None

    def extract(self, default=z3c.form.interfaces.NOVALUE):
        # get normal input fields
        date = self.request.get(self.name + '-date', default)

        if date != default:
            return date

        # get a hidden value
        formatter = self.request.locale.dates.getFormatter("date", "short")
        hidden_date = self.request.get(self.name, '')
        try:
            dateobj = formatter.parse(hidden_date)
            return (str(dateobj.year),
                    str(dateobj.month),
                    str(dateobj.day))
        except DateTimeParseError:
            pass

        return default


@component.adapter(schema.interfaces.IField, z3c.form.interfaces.IFormLayer)
@interface.implementer(z3c.form.interfaces.IFieldWidget)
def DateFieldWidget(field, request):
    """IFieldWidget factory for DateWidget."""
    return z3c.form.widget.FieldWidget(field, DateWidget(request))
