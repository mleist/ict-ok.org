# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of PhysicalConnector"""


__version__ = "$Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, List, TextLine

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IPhysicalLink(Interface):
    """A PhysicalConnector object."""

    connectorPinout = TextLine(
        max_length = 80,
        title = _("Connector pinout"),
        required = False)

#    room = Choice(
#        title=_(u'Room'),
#        vocabulary='AllRooms',
#        required=False
#        )
    
#    local = Choice(
#        title=_(u'Connected from'),
#        vocabulary='AllPhysicalConnectors',
#        required=False
#        )

    connectors = List(
        title=_(u'Connected to'),
        value_type=Choice(vocabulary='AllUnusedOrUsedPhysikalLinkPhysicalConnectors'),
        default=[],
        required = False)
    


#class IPhysicalConnectorFolder(ISuperclass, IFolder):
#    """Container for PhysicalConnector objects
#    """
#
#
#class IAddPhysicalConnector(Interface):
#    """Interface for all Objects"""
#    template = Choice(
#        title = _("Template"),
#        vocabulary="AllPhysicalConnectorTemplates",
#        required = False)


class IPhysicalLinkFolder(Interface):
    """Container for PhysicalLink objects
    """


class IAddPhysicalLink(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllPhysicalLinkTemplates",
        required = False)

class ICreatePhysicalLinks(Interface):
    """A PhysicalConnector object."""
    connectors = List(
        title=_(u'Connected to'),
        value_type=Choice(vocabulary='AllUnusedOrUsedPhysikalLinkPhysicalConnectors'),
        default=[],
        required = False)

