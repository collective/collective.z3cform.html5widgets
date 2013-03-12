import z3c.form
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary


class IStepWidget(z3c.form.interfaces.IWidget):
    """Step support for z3c.form
    HTML5 support of step on
    * input type number, date, time
    """
    step = schema.Int(title=u"Step", required=False)


class IPlaceholder(z3c.form.interfaces.IWidget):
    """
    Supported on:
    * <input> : type text, search, password, url, tel, email
    * <textarea>
    """
    placeholder = schema.TextLine(title=u"Placeholder", required=False)


required_vocab = SimpleVocabulary.fromValues(['required'])


class IRequiredWidget(z3c.form.interfaces.IWidget):
    """
    Supported on:

    * <input> : de type text, search, password, url, tel, email, date,
       datetime, datetime-local, month, week, time, number, checkbox, radio,
       file
    * <textarea>
    """
    required_attr = schema.Choice(title=u"Required (attribute)",
                                  required=False,
                                  vocabulary=required_vocab)


class IPatternWidget(z3c.form.interfaces.IWidget):
    """Add the pattern attributes
    Supported on:
    * <input> type: text, search, password, url, tel, email.
    """

    pattern = schema.ASCIILine(title=u"Pattern", required=False)


class IMinMaxWidget(z3c.form.interfaces.IWidget):
    """Min max attributes
    Supported on:
    * input type number, date, range
    """
    min = schema.ASCIILine(title=u"Min", required=False)
    max = schema.ASCIILine(title=u"Max", required=False)
