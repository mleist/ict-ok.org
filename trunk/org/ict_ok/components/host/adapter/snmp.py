# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of snmp-methods
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.admin_utils.snmpd.interfaces import ISnmptrapd
from org.ict_ok.components.host.interfaces import IHost

# pysnmp imports
from pysnmp.v4.proto import api


class Snmptrapd(object):
    """Ticker-Adapter."""

    implements(ISnmptrapd)
    adapts(IHost)

    def __init__(self, context):
        print "Snmptrapd.__init__ host"
        self.context = context

    def triggered(self, reqPDU, msgVer, pMod):
        """
        got ticker event from ticker thread
        """
        #import pdb;pdb.set_trace()
        print "Snmptrapd %s triggered (reqPDU:%s)!!" % (self.context, reqPDU)
        print '-' * 80
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                print 'Enterprise: %s' % (
                    pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                    )
                print 'Agent Address: %s' % (
                    pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                    )
                print 'Generic Trap: %s' % (
                    pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                    )
                print 'Specific Trap: %s' % (
                    pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                    )
                print 'Uptime: %s' % (
                    pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                    )
                varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
            else:
                varBinds = pMod.apiPDU.getVarBindList(reqPDU)
            if len(varBinds) > 0:
                print 'Var-binds:'
                for oid, val in varBinds:
                    print '-' * 40
                    print '%s = %s' % (oid.prettyPrint(), val.prettyPrint())
                    print '-' * 40
        print '-' * 80
