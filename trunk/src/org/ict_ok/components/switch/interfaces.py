# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of Switch"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class ISwitch(Interface):
    """A Switch object."""

    ifCount = Int(
        title = _(u'Interface quantity'),
        description = _(u'Quantity of all interfaces in this switch'),
        required = False)
        

    rack = Choice(
        title = _(u'Rack'),
        vocabulary = 'AllRacks',
        required = False)
        
#    interfaces = List(
#        title = _(u'Interfaces'),
#        value_type=Choice(vocabulary='AllUnusedOrUsedPhysicalConnectorInterfaces'),
#        default=[],
#        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class ISwitchFolder(Interface):
    """Container for Switch objects
    """


class IAddSwitch(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllSwitchTemplates",
        required = False)
