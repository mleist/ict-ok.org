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
from org.ict_ok.components.host.adapter.snmp import Snmptrapd as BaseSnmptrapd
from org.ict_ok.components.host.special.mge_ups.interfaces import IHostMgeUps

# pysnmp imports
from pysnmp.v4.proto import api


class Snmptrapd(BaseSnmptrapd):
    """Ticker-Adapter."""

    implements(ISnmptrapd)
    adapts(IHostMgeUps)

    def __init__(self, context):
        print "Snmptrapd.__init__ mge_ups"
        self.context = context

    def triggered(self, reqPDU, msgVer, pMod):
        """
        got ticker event from ticker thread
        """
        #print "Snmptrapd %s triggered (reqPDU:%s)!!" % (self.context, reqPDU)
        #print '-' * 80
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                #print 'Enterprise: %s' % (
                    #pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                    #)
                #print 'Agent Address: %s' % (
                    #pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                    #)
                #print 'Generic Trap: %s' % (
                    #pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                    #)
                #print 'Specific Trap: %s' % (
                    #pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                    #)
                #print 'Uptime: %s' % (
                    #pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                    #)
                varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
                # TODO remove this big fake
                if pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint() == \
                   u'1.3.6.1.4.1.207.1.4.29':
                    print "AT - Switch!!!"
                    if pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint() == 'linkUp(3)':
                        print "1111a"
                        self.context.eventOut_powerReturned()
                    if pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint() == 'linkDown(2)':
                        print "1111b"
                        self.context.eventOut_onBattery()
            else:
                varBinds = pMod.apiPDU.getVarBindList(reqPDU)
            #if len(varBinds) > 0:
                #print 'Var-binds:'
                #for oid, val in varBinds:
                    #print '-' * 40
                    #print '%s = %s' % (oid.prettyPrint(), val.prettyPrint())
                    #print '-' * 40
        #print '-' * 80
