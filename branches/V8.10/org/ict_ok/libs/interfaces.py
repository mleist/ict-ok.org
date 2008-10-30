# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of Codetemplate"""

__version__ = "$Id$"

# zope imports
from zope.schema import TextLine
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass

_ = MessageFactory('org.ict_ok')


class ICodetemplate(ISuperclass):
    """A template object."""

    ikAttr = TextLine(
        min_length = 2,
        max_length = 40,
        title = _("Attribute"),
        description = _("Attribute of the instance."),
        readonly = False,
        required = False)

    def method(self, arg1):
        """
        this instance method does ....
        """
