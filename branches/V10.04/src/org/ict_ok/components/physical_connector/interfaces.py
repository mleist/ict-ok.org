# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of PhysicalConnector"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, List, TextLine

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IPhysicalConnector(Interface):
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

#    link = Choice(
#        title=_(u'Connected to'),
#        vocabulary='AllPhysicalLinks',
#        required=False
#        )

    links = List(
        title=_(u'Connected to'),
        value_type=Choice(vocabulary='AllPhysicalLinks'),
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
