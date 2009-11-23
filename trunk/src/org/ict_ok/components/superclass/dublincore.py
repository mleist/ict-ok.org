# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0212
#
"""subscriber for dublin core properties
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.component import adapter
from zope.dublincore.interfaces import IWriteZopeDublinCore, \
     IZopeDublinCore
from zope.lifecycleevent.interfaces import IObjectCreatedEvent, \
     IObjectModifiedEvent
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass

_ = MessageFactory('org.ict_ok')


@adapter(ISuperclass, IObjectModifiedEvent)
def updateSuperclassDCTitle(ikObject, event):
    """
    Update an object's Dublin Core Title and back
    """
    for i in event.descriptions:
        if ISuperclass.isEqualOrExtendedBy(i.interface):
            dcore = IWriteZopeDublinCore(ikObject)
            dcore.title = ikObject.ikName
        if IZopeDublinCore.isEqualOrExtendedBy(i.interface):
            dcore = IZopeDublinCore(ikObject)
            ikObject.ikName = dcore.title

@adapter(ISuperclass, IObjectCreatedEvent)
def createSuperclassDCTitle(ikObject, event):
    """
    Sets an object's Dublin Core Title
    """
    dcore = IWriteZopeDublinCore(ikObject)
    dcore.title = ikObject.ikName
