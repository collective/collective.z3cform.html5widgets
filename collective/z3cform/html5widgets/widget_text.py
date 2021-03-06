#-*- coding: utf-8 -*-

from zope import schema
from zope import interface
import z3c.form.browser.widget
import z3c.form.widget
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets import base
from zope.i18nmessageid.message import MessageFactory

_ = MessageFactory("collective.z3cform.html5widgets")


class ITextWidget(base.IHTML5InputWidget, z3c.form.interfaces.IWidget):
    """ Text widget marker for z3c.form"""


class ITextLineField(schema.interfaces.ITextLine):
    """ Special marker for date fields that use our widget """


class TextWidget(base.HTML5InputWidget, z3c.form.widget.Widget):
    """widget"""

    interface.implementsOnly(ITextWidget)

    klass = u'html5-text-widget'
    input_type = "text"

    def update(self):
        super(TextWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def TextFieldWidget(field, request):
    """IFieldWidget factory for SearchWidget."""
    return z3c.form.widget.FieldWidget(field, TextWidget(request))


class TextValidationError(schema.ValidationError, ValueError):
    __doc__ = _(u"Please enter a valid text line.")


class Converter(BaseDataConverter):
    """base converter"""

    def toWidgetValue(self, value):
        return value

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value

        try:
            return value
        except ValueError:
            raise TextValidationError
