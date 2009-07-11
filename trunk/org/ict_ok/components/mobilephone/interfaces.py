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
"""Interface of MobilePhone"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, TextLine, Date

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IMobilePhone(Interface):
    """A MobilePhone object."""

    #conns = List(title=u"Conns 0..n",
                 ##value_type=Object(IObject),
                 #value_type=Choice(vocabulary='AllMobilePhones'),
                 #required=False,
                 #default=[])
    #conn = Choice(
        #title=u'Conn 0..1',
        #vocabulary='AllMobilePhones',
        #required=False
        #)
    #related = schema.List(
            #title=u"Related",
            #value_type=schema.Choice(vocabulary='demo.documentsInParent'),
            #required=False,
            #default=[])

    #attrFoo = TextLine(
        #max_length = 80,
        #title = _("Foo"),
        #description = _("Foo of the system."),
        #default = _("default foo"),
        #required = True)

    ##Telefonnummer
    phoneNumber = TextLine(
        max_length = 80,
        title = _("phone number"),
        description = _("phone number"),
        required = True)
    
    #Name
    user = Choice(
        title = _("User"),
        description = _("User of the mobile phone"),
        vocabulary="AllLdapUser",
        required = False)
    
    ##Vertragsmodell
    contractModel = TextLine(
        max_length = 80,
        title = _("contract model"),
        description = _("contract model"),
        required = False)
    
    ##Vertragsende
    contractEnd = Date(
        title = _("contract end date"),
        description = _("contract end date"),
        required = False)
    
    ##Lieferdatum
    deliveryDate = Date(
        title = _("delivery date"),
        description = _("delivery date"),
        required = False)
    
    ##Modell
    modelType = TextLine(
        max_length = 80,
        title = _("model type"),
        description = _("model type"),
        required = False)
    
    ##Seriennummer
    serialNumber = TextLine(
        max_length = 80,
        title = _("Serial number"),
        description = _("Serial number"),
        required = False)
    
    ##IMEI
    imei = TextLine(
        max_length = 40,
        title = _("IMEI"),
        description = _("International Mobile Equipment Identity"),
        required = False)
    
    ##PIN
    pin = TextLine(
        max_length = 20,
        title = _("PIN"),
        description = _("Personal Identification Number"),
        required = False)

    
    puk = TextLine(
        max_length = 20,
        title = _("PUK"),
        description = _("Personal Unblocking Key"),
        required = False)

    
    ##SIM-Nr.
    simNumber = TextLine(
        max_length = 80,
        title = _("SIM number"),
        description = _("Subscriber Identity Module Number"),
        required = False)
    
    def trigger_online():
        """
        trigger workflow
        """


class IMobilePhoneFolder(Interface):
    """Container for MobilePhone objects
    """

class IAddMobilePhone(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllMobilePhoneTemplates",
        required = False)
