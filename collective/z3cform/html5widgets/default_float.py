from zope import schema
from z3c.form.converter import BaseDataConverter
from zope.i18nmessageid.message import MessageFactory

_ = MessageFactory("collective.z3cform.html5widgets")


class IFloat(schema.interfaces.IFloat):
    """ Special marker for date fields that use our widget """


class FloatValidationError(schema.ValidationError, ValueError):
    __doc__ = _(u"Please enter a valid float number: 50.13.")


class Converter(BaseDataConverter):

    def toWidgetValue(self, value):
        return value

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value

        try:
            return float(value)
        except ValueError:
            raise FloatValidationError
