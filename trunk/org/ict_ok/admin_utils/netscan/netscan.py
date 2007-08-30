# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""implementation of a "Network-Scanner-Utility" 
"""

__version__ = "$Id$"

# phython imports
import logging

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.netscan.interfaces import IScanner
from org.ict_ok.admin_utils.netscan.interfaces import INetScan

logger = logging.getLogger("NetScan")


class NetScan(Supernode):
    """implementation of a "Network-Scanner-Utility" """

    implements(INetScan)

    scannerSet = FieldProperty(INetScan['scannerSet'])

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__
        #self.scannerSet = Set([u"AdmUtilNMap"])
        
    def getAllScannerObjs(self):
        """
        get list of all Scanner-Tupel (name, obj)
        """
        return [(name, obj) for (name, obj) in \
                zapi.getUtilitiesFor(IScanner)]

    def getScannerObjs(self):
        """
        get list of enabled Scanner-Tupel (name, obj)
        """
        return [(name, obj) for (name, obj) \
                in zapi.getUtilitiesFor(IScanner) \
                if obj.__name__ in self.scannerSet]


def NetScannerInstances(dummy_context):
    """Which types of network scanners are there
    """
    #print "NetScannerInstances   ################"
    utilList = [util for name, util in zapi.getUtilitiesFor(IScanner)]
    #prefixes = [u'dot', u'neato', u'twopi', u'circo', u'fdp']
    terms = [SimpleTerm(i.__name__, str(i.__name__), i.__name__) \
             for i in utilList]
    return SimpleVocabulary(terms)
