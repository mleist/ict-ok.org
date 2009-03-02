# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0213,E0211,W0232
#
"""Interface of Latency"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Int

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class ILatency(Interface):
    """A service object."""

    checkcount = Int(
        title = _(u"Check count"),
        default = 20,
        required = True)

class IMuninValueFolder(Interface):
    """Container for MuninValue objects
    """

class IAddMuninValue(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllMuninValueTemplates",
        required = False)
