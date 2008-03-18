# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of Service"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.schema import Int

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class IService(IComponent):
    """A service object."""

    port = Int(
        min = 1,
        max = 65535,
        title = _("Port"),
        description = _("Number of port."),
        default = 65535,
        required = True)
