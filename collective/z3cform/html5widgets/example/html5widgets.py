from zope import component
from zope import schema
from zope import interface
from Products.Five import BrowserView
from z3c.form import form, button, field
from plone.z3cform import layout


class ExampleSchema(interface.Interface):
    date = schema.Date(title=u"date example")


class ExampleAdapter(object):
    interface.implements(ExampleSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context

    def get_date(self):
        return self.context.created().asdatetime()

    def set_date(self, value):
        self.context.setCreationDate(value)

    date = property(get_date, set_date)


class ExampleForm(form.Form):
    """example"""
    fields = field.Fields(ExampleSchema)

    @button.buttonAndHandler(u'Ok')
    def handle_ok(self, action):
        data, errors = self.extractData()
        print data, errors

Example = layout.wrap_form(ExampleForm)
