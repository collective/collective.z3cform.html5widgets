#-*- coding: utf-8 -*-

from zope import interface
import z3c.form.browser.widget
import z3c.form.widget
from collective.z3cform.html5widgets import base
from zope.i18nmessageid.message import MessageFactory

_ = MessageFactory("collective.z3cform.html5widgets")


class INumberWidget(base.IHTML5InputWidget, z3c.form.interfaces.IWidget):
    """ Number widget marker for z3c.form """


class NumberWidget(base.HTML5InputWidget, z3c.form.widget.Widget):
    """Widget"""

    interface.implementsOnly(INumberWidget)

    klass = u'html5-number-widget'
    input_type = "number"

    def update(self):
        super(NumberWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def NumberFieldWidget(field, request):
    """IFieldWidget factory for NumberWidget."""
    return z3c.form.widget.FieldWidget(field, NumberWidget(request))
