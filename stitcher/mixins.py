# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class UnicodeStrMixin(object):
    """
    Gives a class defining a `__unicode__()` method a `__str__()` method.
    """

    def __str__(self):
        return unicode(self).encode('utf-8')
