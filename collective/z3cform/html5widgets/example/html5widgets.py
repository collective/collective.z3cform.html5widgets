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
        self.date = None


class ExampleForm(form.Form):
    """example"""
    fields = field.Fields(ExampleSchema)

    @button.buttonAndHandler(u'Ok')
    def handle_ok(self, action):
        data, errors = self.extractData()
        print data, errors

Example = layout.wrap_form(ExampleForm)
