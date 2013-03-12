from zope import component
from zope import schema
from zope import interface
from z3c.form import form, button, field
from plone.z3cform import layout
from collective.z3cform.html5widgets.widget_tel import TelFieldWidget
from collective.z3cform.html5widgets.widget_month import MonthFieldWidget
from collective.z3cform.html5widgets.widget_number import NumberFieldWidget


class ExampleSchema(interface.Interface):
    date = schema.Date(title=u"Date (created)", required=False)
    datetime = schema.Datetime(title=u"Date time (modified)", required=False)
    datetime_local = schema.Datetime(title=u"Date time local (modified)", required=False)
    month = schema.Date(title=u"Month", required=False)
    number = schema.Int(title=u"Number", required=False)
    tel = schema.ASCIILine(title=u"Telephone", required=False)
    time = schema.Time(title=u"Time", required=False)
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
    fields['month'].widgetFactory = MonthFieldWidget
    fields['number'].widgetFactory = NumberFieldWidget

    @button.buttonAndHandler(u'Ok')
    def handle_ok(self, action):
        data, errors = self.extractData()
        print data, errors

Example = layout.wrap_form(ExampleForm)
