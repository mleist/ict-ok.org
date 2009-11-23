# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
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
from zope.interface import Interface
from zope.schema import TextLine
from zope.i18nmessageid import MessageFactory
from zope.app.container.constraints import contains

# ict_ok imports

_ = MessageFactory('org.ict_ok')


class ISlave(Interface):
    """A objectcontainer for new slave data."""

    contains('org.ict_ok.components.ipnet.interfaces.IIpNet')

    title = TextLine(
        min_length = 2,
        max_length = 40,
        title = u"Title/Subject",
        description = u"Title and/or subject of the message.",
        default = u"Title",
        required = True)

class INewSlaveEvent(Interface):
    """
    Indicates that a new ICT_Ok slave node has been created
    """
