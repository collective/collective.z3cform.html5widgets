###############################################################################
#
# Copyright 2006 by refline (Schweiz) AG, CH-5630 Muri
#
###############################################################################

"""
$Id: tests.py 86815 2008-05-17 00:53:17Z pcardune $
"""
__docformat__ = "reStructuredText"

import doctest
import unittest
from zope.testing.doctestunit import DocFileSuite

from z3c.form import testing


def test_suite():
    tests = []
    tests.append(DocFileSuite('tests/widget_color.txt',
                 setUp=testing.setUp, tearDown=testing.tearDown,
                 optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
                 ),
     )
    tests.append(DocFileSuite('tests/widget_contenteditable.txt',
                 setUp=testing.setUp, tearDown=testing.tearDown,
                 optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
                 ),
     )
    tests.append(DocFileSuite('tests/widget_date.txt',
                 setUp=testing.setUp, tearDown=testing.tearDown,
                 optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
                 ),
    )
    tests.append(DocFileSuite('tests/widget_text.txt',
                 setUp=testing.setUp, tearDown=testing.tearDown,
                 optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
                 ),
    )
    return unittest.TestSuite(tests)
