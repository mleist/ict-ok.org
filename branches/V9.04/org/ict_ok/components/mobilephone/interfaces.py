# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
from pyExcelerator.BIFFRecords import CodepageBiff8Record
"""Interface of MobilePhone"""


__version__ = "$Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# zope imports
from zope.interface import Attribute, Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine, Bytes, Date
from zope.app.folder.interfaces import IFolder

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class IImportXlsData(Interface):
    """Interface for all Objects"""
    xlsdata = Bytes(
        title = _("XLS data"),
        required = True)
    
    codepage = Choice(
        title = _("Codepage"),
        description = _("Codepage of XLS"),
        vocabulary="AllXlsCodepages",
        default = 'cp850',
        required = True)


class IImportCsvData(Interface):
    """Interface for all Objects"""
    csvdata = Bytes(
        title = _("CSV data"),
        required = True)


class IMobilePhone(IComponent):
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


class IMobilePhoneFolder(ISuperclass, IFolder):
    """Container for MobilePhone objects
    """
