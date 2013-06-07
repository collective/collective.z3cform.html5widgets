Introduction
============

This addon provide many HTML5 form features to z3c.form.

BE WARNED: this addon is quite young, use it at your own risk.

Badges
======


.. image:: https://pypip.in/v/collective.z3cform.html5widgets/badge.png
    :target: https://crate.io/packages/collective.z3cform.html5widgets/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/collective.z3cform.html5widgets/badge.png
    :target: https://crate.io/packages/collective.z3cform.html5widgets/
    :alt: Number of PyPI downloads

.. image:: https://secure.travis-ci.org/toutpt/collective.z3cform.html5widgets.png
    :target: http://travis-ci.org/#!/toutpt/collective.z3cform.html5widgets

.. image:: https://coveralls.io/repos/toutpt/collective.z3cform.html5widgets/badge.png?branch=master
    :alt: Coverage
    :target: https://coveralls.io/r/toutpt/collective.z3cform.html5widgets


Widgets
=======

* color
* contenteditable (+wysiwyg)
* date
* datetime
* datetime-local
* email
* month
* number
* password
* range
* search
* tel
* time
* url
* week

New input attributes
====================

This addon provide a base class HTML5InputWidget which support the following
new attributes:

* autocomplete
* min
* max
* pattern
* placeholder
* required
* step

So overriding the update method you can add values to theses values. By default
the HTML5InputWidget base class do some test around support of theses
attributes depending on the input's type.

required is automaticly bind on the field's required value.

step is automaticly set to "any" for decimal and float values.


Bind on zope.schema fields
==========================

* Date -> date
* DateTime -> datetime-local
* Decimal -> number
* Int -> number
* Password -> password
* Time -> time
* URI -> url

TODO
====

* add tests
* add support of datalist

How to install
==============

This addon can be installed has any other addons. please follow official
documentation_. It doesn't provide any profile, so you juste have to add it
to your zope install.

If you want to support theses widgets on incapable browser you must consider
using polyfill.

Some addons which provide polyfills:

* collective.js.webshims

Credits
=======

Companies
---------

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact Makina Corpus <mailto:python@makina-corpus.org>`_

People
------

- JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>

.. _documentation: http://plone.org/documentation/kb/installing-add-ons-quick-how-to
