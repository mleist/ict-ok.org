# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232,W0622
#
"""Interface of ICT_Ok ikslave
"""

__version__ = "$Id$"

# zope imports
from zope.schema import TextLine
from zope.i18nmessageid import MessageFactory
from zope.app.container.constraints import contains
from zope.component.interfaces import IObjectEvent
from zope.app.component.interfaces import IPossibleSite

# ict_ok imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class ISlave(IPossibleSite, ISupernode):
    """A objectcontainer for new slave data."""

    contains('org.ict_ok.components.net.interfaces.INet')

    title = TextLine(
        min_length = 2,
        max_length = 40,
        title = u"Title/Subject",
        description = u"Title and/or subject of the message.",
        default = u"Title",
        required = True)

class INewSlaveEvent(IObjectEvent):
    """
    Indicates that a new ICT_Ok slave node has been created
    """
