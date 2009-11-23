# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0201,R0201
#
"""
python package
"""
__version__ = "$Id$"

# python imports
import sys
import traceback

# zope imports
from zope.interface import implements
from zope.app.exception.interfaces import ISystemErrorView

# z3c imports
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports


class MySystemErrorView:
    """adapter for the error view"""
    implements(ISystemErrorView)

    def isSystemError(self):
        """ ... """
        return True


class IkErrorForm(BrowserPagelet, MySystemErrorView):
    """ Error Pagelet """
    def update(self):
        """store error data / traceback for pagelet"""
        self.error_type, self.error_object, tr_back = sys.exc_info()
        try:
            self.traceback_lines = traceback.format_tb(tr_back)
        finally:
            del tr_back
