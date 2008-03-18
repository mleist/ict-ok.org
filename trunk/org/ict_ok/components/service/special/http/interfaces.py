# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <->
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py 73 2007-10-02 09:37:48Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of Service Http"""


__version__ = "$Id: interfaces.py 73 2007-10-02 09:37:48Z markusleist $"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.schema import Int

# ict_ok.org imports
from org.ict_ok.components.service.interfaces import IService

_ = MessageFactory('org.ict_ok')


class IServiceHttp(IService):
    """http service

A http service check object.

    """

    port = Int(
        min = 1,
        max = 65535,
        title = _("Port"),
        description = _("Number of port."),
        default = 80,
        required = True)
