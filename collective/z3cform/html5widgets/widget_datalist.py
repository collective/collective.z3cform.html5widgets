#python
from datetime import datetime

#zope
from zope import schema
from zope import interface
from zope import component
from zope.schema.fieldproperty import FieldProperty
import z3c.form.browser.widget
import z3c.form.widget
from z3c.form.converter import BaseDataConverter

#plone
from plone.app.z3cform import widget

#internal
from collective.z3cform.html5widgets import attributes
from plone.formwidget.autocomplete.widget import AutocompleteSelectionWidget
from plone.formwidget.autocomplete.interfaces import IAutocompleteWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IDatalistSelectionWidget(attributes.IRequiredWidget, IAutocompleteWidget):
    """Datalist widget marker for z3c.form """


class DatalistSelectionWidget(AutocompleteSelectionWidget):
    """HTML Datalist widget:"""
    input_template = ViewPageTemplateFile('templates/datalist_input.pt')

    interface.implementsOnly(IDatalistSelectionWidget)

    klass = u'html5-date-widget'
    required_attr = FieldProperty(IDatalistSelectionWidget['required_attr'])
    js_callback_template = """\
    (function($) {
        $().ready(function() {
            $('#%(id)s-input-fields').data('klass','%(klass)s').data('title','%(title)s').data('input_type','%(input_type)s');
            $('#%(id)s-buttons-search').remove();

            %(js_extra)s
        });
    })(jQuery);
    """

    def update(self):
        super(DatalistSelectionWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)



@interface.implementer(z3c.form.interfaces.IFieldWidget)
def DatalistSelectionFieldWidget(field, request):
    """IFieldWidget factory for DatalistWidget."""
    return z3c.form.widget.FieldWidget(field, DatalistSelectionWidget(request))
