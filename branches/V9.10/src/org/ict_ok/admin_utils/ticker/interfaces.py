# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=W0232
#
"""Interface of Object-Message-Queue-Utility"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Set

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import \
     IEventIfSupernode

_ = MessageFactory('org.ict_ok')


class IAdmUtilTicker(Interface):
    """A pseudo-mailer that delivers objects by xmlrpc."""

class IEventIfAdmUtilTicker(IEventIfSupernode):
    """ event interface of object """
    eventOutObjs_1sec = Set(
        title = _("1sec. event ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)
    def eventOut_1sec(self):
        """ sends one-second event """
