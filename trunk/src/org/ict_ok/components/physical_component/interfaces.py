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
"""Interface of PhysicalComponent"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface, Invalid, invariant
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, TextLine

# ict_ok.org imports
from org.ict_ok.schema.date import Date

_ = MessageFactory('org.ict_ok')


class IPhysicalComponent(Interface):
    """A PhysicalComponent object."""

#    room = Choice(
#        title=_(u'Room'),
#        vocabulary='AllRooms',
#        required=False
#        )
    user = Choice(
        title = _("User"),
        description = _("User of the mobile phone"),
        vocabulary="AllLdapUser",
        required = False)

    manufacturer = TextLine(#
        max_length = 200,
        title = _("Manufacturer"),
        description = _("Name/Address of the manufacturer."),
        required = False)

    modelType = TextLine(#
        title = _(u'Model type'),
        description = _(u'model type'),
        required = False)

    vendor = TextLine(#
        max_length = 500,
        title = _("Vendor"),
        description = _("Name/Address of the vendor."),
        default = u"",
        required = False)
    
    deliveryDate = Date(#
        title = _(u'Delivery date'),
        description = _(u'delivery date'),
        required = False)
        
    room = Choice(#
        title=_(u'Room'),
        vocabulary='AllRooms',
        required=False
        )

    serialNumber = TextLine(#
        title = _(u'Serial number'),
        description = _(u'Serial number'),
        required = False)
        
    inv_id = TextLine(#
        title = _(u'Inventory id'),
        description = _(u'Id of inventory.'),
        required = False)

    documentNumber = TextLine(#
        title = _(u'Document number'),
        description = _(u'Document number'),
        required = False)

    productionState = Choice(
        title = _("Production state"),#
        vocabulary="AllHostProductionStates",
        default = 'production',
        readonly = False,
        required = True)

    @invariant
    def ensureRoomInvariants(event):
        if hasattr(event.__context__, 'ensureInvariants'):
            event.__context__.ensureInvariants(event)
