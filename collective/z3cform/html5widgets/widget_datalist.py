#zope
from zope import interface
import z3c.form.interfaces
import z3c.form.widget

#plone
from plone.formwidget.contenttree.interfaces import IContentTreeWidget
from plone.formwidget.contenttree.widget import MultiContentTreeWidget


from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.converter import BaseDataConverter
from collective.z3cform.html5widgets.base import IHTML5InputWidget,\
    HTML5InputWidget
from z3c.form.browser.widget import addFieldClass

#internal


class IMultiDatalistWidget(
        IContentTreeWidget,
        IHTML5InputWidget,
        z3c.form.interfaces.IWidget):
    """Datalist widget marker for z3c.form """


class MultiDatalistWidget(
        MultiContentTreeWidget,
        HTML5InputWidget,
        z3c.form.widget.Widget):
    interface.implementsOnly(IMultiDatalistWidget)
    input_template = ViewPageTemplateFile('templates/datalist_input.pt')

    klass = u'html5-datalist-multiselection-widget'
    js_template = """\
    (function($) {
        $().ready(function() {
            console.log('autocomplete ready ?');
        });
    })(jQuery);
    """

    def update(self):
        super(MultiDatalistWidget, self).update()
        addFieldClass(self)

    def js_extra(self):
        return ""


@interface.implementer(z3c.form.interfaces.IFieldWidget)
def MultiDatalistFieldWidget(field, request):
    """IFieldWidget factory for DatalistWidget."""
    return z3c.form.widget.FieldWidget(field, MultiDatalistWidget(request))


class Converter(BaseDataConverter):

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return None
        return value

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value

        try:
            return str(value)
        except ValueError:
            raise Exception
