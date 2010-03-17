# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of Address"""


__version__ = "$Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IAddress(Interface):
    """A Address object."""

    address1 = TextLine(
        title = _(u'Address1'),
        description = _(u"Address line 1"),
        required = False)
        
    address2 = TextLine(
        title = _(u'Address2'),
        description = _(u"Address line 2"),
        required = False)
        
    address3 = TextLine(
        title = _(u'Address3'),
        description = _(u"Address line 3"),
        required = False)
        
    city = TextLine(
        title = _(u'City'),
        description = _(u"City"),
        required = False)
        
    postalCode = TextLine(
        title = _(u'Postal code'),
        description = _(u"Postal code"),
        required = False)
        
    country = TextLine(
        title = _(u'Country'),
        description = _(u"Country"),
        required = False)
        

#    contactItem = Choice(
#        title = _(u'Contact item'),
#        vocabulary = 'AllContactItems',
#        required = False)
#    
    contactItems = List(
        title = _(u'Contact items'),
        value_type=Choice(vocabulary='AllContactItems'),
        default=[],
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IAddressFolder(Interface):
    """Container for Address objects
    """


class IAddAddress(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllAddressTemplates",
        required = False)
