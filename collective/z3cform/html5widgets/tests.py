import doctest
import unittest
from zope.testing.doctestunit import DocFileSuite

from z3c.form import testing


def test_suite():
    tests = []
    for test in (
        'color', 'contenteditable', 'date', 'datetime',
        'datetimelocal', 'email',
        'text'):
        filename = 'tests/widget_%s.txt' % test
        tests.append(DocFileSuite(filename,
                 setUp=testing.setUp, tearDown=testing.tearDown,
                 optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
                 ),
         )
    return unittest.TestSuite(tests)
