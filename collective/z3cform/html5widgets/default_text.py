from zope import schema
from zope.i18nmessageid.message import MessageFactory
from z3c.form.converter import BaseDataConverter

_ = MessageFactory("collective.z3cform.html5widgets")


class IText(schema.interfaces.IText):
    """ Special marker for date fields that use our widget """


class ContentEditableValidationError(schema.ValidationError, ValueError):
    __doc__ = _(u"Please enter a valid html content")


class Converter(BaseDataConverter):

    def toWidgetValue(self, value):
        return value

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value

        try:
            return value
        except ValueError:
            raise ContentEditableValidationError
