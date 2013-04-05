#-*- coding: utf-8 -*-

from zope import interface
import z3c.form.interfaces
import z3c.form.browser.widget
import z3c.form.widget


class IContentEditableWidget(z3c.form.interfaces.IWidget):
    """ ContentEditable widget marker for z3c.form"""


class ContentEditableWidget(z3c.form.browser.widget.HTMLTextInputWidget,
                z3c.form.widget.Widget):
    """HTML  widget:
    """

    interface.implementsOnly(IContentEditableWidget)

    klass = u'html5-contenteditable-widget'

    def update(self):
        super(ContentEditableWidget, self).update()
        z3c.form.browser.widget.addFieldClass(self)


def ContentEditableFieldWidget(field, request):
    """IFieldWidget factory for ContentEditableWidget."""
    return z3c.form.widget.FieldWidget(field, ContentEditableWidget(request))
