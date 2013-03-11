import z3c.form
import z3c.form.interfaces
import zope.schema


class IDateField(zope.schema.interfaces.IDate):
    """ Special marker for date fields that use our widget """


# Widgets

class IDateWidget(z3c.form.interfaces.IWidget):
    """ Date widget marker for z3c.form """
