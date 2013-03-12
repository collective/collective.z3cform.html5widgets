from zope import component
from zope import schema
from zope import interface
from z3c.form import form, button, field
from plone.z3cform import layout


class ExampleSchema(interface.Interface):
    created = schema.Date(title=u"Date (created)")
    modified = schema.Datetime(title=u"Date time (modified)")


class ExampleAdapter(object):
    interface.implements(ExampleSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context

    def get_created(self):
        return self.context.created().asdatetime()

    def set_created(self, value):
        self.context.setCreationDate(value)

    created = property(get_created, set_created)

    def get_modified(self):
        return None  # self.context.modified().asdatetime()

    def set_modified(self, value):
        self.context.setModificationDate(value)

    modified = property(get_modified, set_modified)


class ExampleForm(form.Form):
    """example"""
    fields = field.Fields(ExampleSchema)

    @button.buttonAndHandler(u'Ok')
    def handle_ok(self, action):
        data, errors = self.extractData()
        print data, errors

Example = layout.wrap_form(ExampleForm)
