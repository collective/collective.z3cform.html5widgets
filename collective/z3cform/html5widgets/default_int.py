
from zope import schema
from z3c.form.converter import BaseDataConverter
from zope.i18nmessageid.message import MessageFactory

_ = MessageFactory("collective.z3cform.html5widgets")


class IInt(schema.interfaces.IInt):
    """ Special marker for date fields that use our widget """


class IntValidationError(schema.ValidationError, ValueError):
    __doc__ = _(u"Please enter a valid number: 50.")


class Converter(BaseDataConverter):

    def toWidgetValue(self, value):
        return value

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value

        try:
            return int(value)
        except ValueError:
            raise IntValidationError
