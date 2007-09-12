# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""
'mail' ZCML Namespaces Schemas
implementation of a "Object-Message-Queue-Utility" 
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import Interface
from zope.schema import TextLine
from zope.security.zcml import Permission

# ict_ok.org imports
from org.ict_ok.admin_utils.ticker.ticker import TickerThread


#def _assertPermission(permission, interfaces, component):
    #if permission is not None:
        #if permission == PublicPermission:
            #permission = CheckerPublic
        #checker = InterfaceChecker(interfaces, permission)

    #return proxify(component, checker)


class IAdmUtilTickerDirective(Interface):
    """This abstract directive describes a generic mail delivery utility
    registration."""

    name = TextLine(
        title=u"Name",
        description=u'Specifies the Name of the ticker utility. '\
                    u'The default is "Ticker".',
        default=u"Ticker",
        required=False)

    permission = Permission(
        title=u"Permission",
        description=u"Defines the permission needed to use this service.",
        required=True)


def admUtilTicker(_context, permission, name="Ticker"):

    def createTicker():
        thread = TickerThread()
        #thread.setMailer(mailerObject)
        #thread.setQueuePath(queuePath)
        thread.start()

    _context.action(
            discriminator = ('delivery', name),
            callable = createTicker,
            args = () )
