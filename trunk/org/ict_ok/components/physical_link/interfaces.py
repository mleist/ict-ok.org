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
from zope.interface import Attribute, Interface, Invalid, invariant
from zope.i18nmessageid import MessageFactory
from zope.schema import Bool, Choice, List, TextLine

# ict_ok.org imports
from org.ict_ok.schema.physicalvalid import PhysicalQuantity
from org.ict_ok.libs.physicalquantity import convertQuantity
#from org.ict_ok.components.physical_link.physical_link import maxLength4LinkType

#
# ToDo: dirty location
#
def maxLength4LinkType(linkType):
    return convertQuantity('100 m');


_ = MessageFactory('org.ict_ok')


class IPhysicalLink(Interface):
    """A PhysicalConnector object."""

    length = PhysicalQuantity(
        max_length = 10,
        title = _(u"Length"),
        description = _(u"The length of the physical link."),
        required = False)

    maxLength = PhysicalQuantity(
        max_length = 10,
        title = _(u"Maximum length"),
        description = _(u"The maximum length of the physical link."),
        required = False)

    mediaType = Choice(
        title=_(u"Media type"),
        description=_(u"The MediaType property defines the particular type "
                      u"of Media through which transmission signals pass."),
        default=6,
        required = True,
        vocabulary = "PhysicalLinkMediaTypes")
    
    wired = Bool(
        title = _(u"Physical link is cable"),
        description = _(u"﻿Boolean indicating whether the PhysicalLink is an "
                        u"actual cable (TRUE) or a "
                        u"wireless connection (FALSE)."),
        default = True,
        required = True)


    connectorPinout = TextLine(
        max_length = 80,
        title = _(u"Connector pinout"),
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

    @invariant
    def ensureLengthUnit(link):
        if link.length is not None:
            physicalInput = convertQuantity(link.length)
            if not physicalInput.isLength():
                raise Invalid(
                    "No length specification: '%s'." % \
                    (link.length))

    @invariant
    def ensureMaxLength4LinkType(link):
        if link.length is not None:
            physicalInput = convertQuantity(link.length)
            physicalMaxLength = maxLength4LinkType(link.mediaType)
            if physicalInput > physicalMaxLength:
                raise Invalid(
                    "Length over: '%s'." % \
                    (physicalMaxLength))

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

