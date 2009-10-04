# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade SnmpValue from gen 0 to gen 1
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.snmpvalue.interfaces import ISnmpValue

generation = 3

def evolve(context):
    u"""
    convert object from hard coded oid1 and oid2 to list of addresses
    """

    root = getRootFolder(context) # the Zope-Root-Folders

    for iksnmpvalue in findObjectsProviding(root, ISnmpValue):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "SNMP Value(%s): " % iksnmpvalue.ikName + evolve_msg
        if iksnmpvalue.oid1 is not None:
            if iksnmpvalue.oid2 is not None:
                if iksnmpvalue.oid1 == iksnmpvalue.oid2:
                    iksnmpvalue.inp_addrs = [iksnmpvalue.oid1]
                else:
                    iksnmpvalue.inp_addrs = [iksnmpvalue.oid1,
                                            iksnmpvalue.oid2]
            else:
                iksnmpvalue.inp_addrs = [iksnmpvalue.oid1]
        else:
            if iksnmpvalue.oid2 is not None:
                iksnmpvalue.inp_addrs = [iksnmpvalue.oid2]
            else:
                iksnmpvalue.inp_addrs = []
        if iksnmpvalue.checktype == u"oid":
            iksnmpvalue.checktype = u"address"
        del iksnmpvalue.oid1
        del iksnmpvalue.oid2
        iksnmpvalue.appendHistoryEntry(evolve_msg)
