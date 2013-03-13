#-*- coding: utf-8 -*-

from zope import schema
from zope import interface
from zope import component
import z3c.form.browser.widget
import z3c.form.widget
from zope.schema.fieldproperty import FieldProperty
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets import attributes


class ISearchWidget(attributes.IRequiredWidget,
                    attributes.IPlaceholder):
    """ Search widget marker for z3c.form
    http://www.w3.org/TR/html-markup/input.search.html

    """


class ISearchField(schema.interfaces.ITextLine):
    """ Special marker for date fields that use our widget """


class SearchWidget(z3c.form.browser.widget.HTMLTextInputWidget,
                z3c.form.widget.Widget):
    """HTML  widget:
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

    interface.implementsOnly(ISearchWidget)

    klass = u'html5-number-widget'
    required_attr = FieldProperty(ISearchWidget['required_attr'])
    placeholder = FieldProperty(ISearchWidget['placeholder'])

    def update(self):
        super(SearchWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def SearchFieldWidget(field, request):
    """IFieldWidget factory for SearchWidget."""
    return z3c.form.widget.FieldWidget(field, SearchWidget(request))


class SearchValidationError(schema.ValidationError, ValueError):
    __doc__ = u'Please enter a valid search term.'


class Converter(BaseDataConverter):

    def toWidgetValue(self, value):
        return value

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value

        try:
            return value
        except ValueError:
            raise SearchValidationError
