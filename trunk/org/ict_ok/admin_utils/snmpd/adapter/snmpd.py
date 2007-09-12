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
"""Adapter implementation of size-methods
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISnmpd
from org.ict_ok.admin_utils.snmpd.interfaces import IAdmUtilSnmpd


class Snmpd(object):
    """Snmpd-Adapter."""

    implements(ISnmpd)
    adapts(IAdmUtilSnmpd)

    def __init__(self, context):
        self.context = context

    def triggered(self):
        """
        got snmpd event from snmpd thread
        """
        print "AdmUtilSnmpd: '%s' triggered!!" % self.context
