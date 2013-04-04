import decimal
from collective.z3cform.html5widgets import widget_number
import z3c.form.widget
from zope import schema
from z3c.form.converter import DecimalDataConverter as ddc,\
    FormatterValidationError, BaseDataConverter


class IDecimalField(schema.interfaces.IDecimal):
    """marker"""


class DecimalWidget(widget_number.NumberWidget):
    step = "any"

    def update(self):
        super(DecimalWidget, self).update()
        self.step = "any"


def DecimalFieldWidget(field, request):
    """IFieldWidget factory for DecimalWidget."""
    return z3c.form.widget.FieldWidget(field, DecimalWidget(request))


class DecimalDataConverter(BaseDataConverter):

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        if value is self.field.missing_value:
            return u''
        return unicode(value)

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        if value == u'':
            return self.field.missing_value
        try:
            return decimal.Decimal(value)
        except decimal.InvalidOperation:
            msg = ddc.errorMessage
            raise FormatterValidationError(msg)
