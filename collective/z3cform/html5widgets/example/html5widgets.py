from zope import component
from zope import schema
from zope import interface
from z3c.form import form, button, field
from plone.z3cform import layout
from collective.z3cform.html5widgets.widget_tel import TelFieldWidget


class ExampleSchema(interface.Interface):
    date = schema.Date(title=u"Date (created)", required=False)
    datetime = schema.Datetime(title=u"Date time (modified)", required=False)
    datetime_local = schema.Datetime(title=u"Date time local (modified)", required=False)
    time = schema.Time(title=u"Time", required=False)
    tel = schema.ASCIILine(title=u"Telephone", required=False)
    #required = schema.ASCIILine(title=u"", required=True)


class ExampleAdapter(object):
    interface.implements(ExampleSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context
        self.date = None
        self.datetime = None
        self.datetime_local = None
        self.tel = None


class ExampleForm(form.Form):
    """example"""
    fields = field.Fields(ExampleSchema)
    fields['tel'].widgetFactory = TelFieldWidget

    @button.buttonAndHandler(u'Ok')
    def handle_ok(self, action):
        data, errors = self.extractData()
        print data, errors

Example = layout.wrap_form(ExampleForm)
