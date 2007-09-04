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
"""Interface of Network-Scanner-Utility"""

__version__ = "$Id$"

# zope imports
from zope.schema import Choice, Set
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class INetScan(ISupernode):
    """
    component for scanning local network
    """
    scannerSet = Set (
        title = _("Network Scanners"),
        description = _("Which network scanners should be triggerd"),
        value_type = Choice(
            title = _("Network Scanner"),
            vocabulary="NetScannerInstances"),
        default=set([]),
        readonly = False,
        required = True)
    
    def getAllScannerObjs(self):
        """
        get list of all Scanner-Tupel (name, obj)
        """

    def getScannerObjs(self):
        """
        get list of enabled Scanner-Tupel (name, obj)
        """

class IScanner(ISupernode):
    """
    abstract scanner for networks
    """
