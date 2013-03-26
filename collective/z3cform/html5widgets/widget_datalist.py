#zope
from zope import interface
import z3c.form.interfaces
import z3c.form.widget

#plone
from plone.formwidget.contenttree.interfaces import IContentTreeWidget
from plone.formwidget.contenttree.widget import MultiContentTreeWidget


from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.relationfield.widget import RelationListDataManager

#internal


class DatalistManager(RelationListDataManager):
    pass


class IMultiDatalistWidget(IContentTreeWidget):
    """Datalist widget marker for z3c.form """


class MultiDatalistWidget(MultiContentTreeWidget):
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

    def js_extra(self):
        return ""

    def render(self):
        if self.mode == z3c.form.interfaces.DISPLAY_MODE:
            return "display"
        elif self.mode == z3c.form.interfaces.HIDDEN_MODE:
            return "hidden"
        else:
            return self.input_template(self)


@interface.implementer(z3c.form.interfaces.IFieldWidget)
def MultiDatalistFieldWidget(field, request):
    """IFieldWidget factory for DatalistWidget."""
    return z3c.form.widget.FieldWidget(field, MultiDatalistWidget(request))
