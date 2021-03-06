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

# pysnmp imports
from pysnmp.v4.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.v4.carrier.asynsock.dgram import udp
from pyasn1.codec.ber import decoder
from pysnmp.v4.proto import api

# ict_ok.org imports
from org.ict_ok.admin_utils.snmpd.snmpd import SnmpdThread


class IAdmUtilSnmpdDirective(Interface):
    """This abstract directive describes a generic mail delivery utility
    registration."""

    name = TextLine(
        title=u"Name",
        description=u'Specifies the Name of the snmpd utility. '\
                    u'The default is "Snmpd".',
        default=u"Snmpd",
        required=False)

    permission = Permission(
        title=u"Permission",
        description=u"Defines the permission needed to use this service.",
        required=True)


def admUtilSnmpd(_context, permission, name="Snmpd"):

    def createSnmpd():
        thread = SnmpdThread()
        thread.setDaemon(1)
        thread.start()

    _context.action(
            discriminator = ('delivery', name),
            callable = createSnmpd,
            args = () )
