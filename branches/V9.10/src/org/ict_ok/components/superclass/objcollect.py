# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""startup of subsystem"""

__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.component import adapter, queryUtility
import zope.component.interfaces
from zope.interface import implements
from zope.app import zapi
from zope.app.zapi import getPath
from zope.lifecycleevent.interfaces import IObjectCopiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.app.intid.interfaces import IIntIds
from ZODB.interfaces import IConnection
from zope.security.proxy import removeSecurityProxy

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import IPickle, \
     ISuperclass, IObjectAddedEvent
from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjMQ
#from org.ict_ok.components.superclass.interfaces import IPickle
#from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
#from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjMQ

logger = logging.getLogger("Compon. Superclass")


class ObjectAddedEvent(zope.component.interfaces.ObjectEvent):
    """An object has been created"""
    implements(IObjectAddedEvent)


@adapter(ISuperclass, IObjectCopiedEvent)
def notifyCopiedEvent(instance, event):
    logger.info(u"superclass.objcollect.notifyCopiedEvent: event: %s" % event)
    raw_instance = removeSecurityProxy(instance)
    connection = IConnection(raw_instance)
    oc = connection.root()['_oq_collection']
    oc.index(raw_instance)
    

@adapter(ISuperclass, IObjectAddedEvent)
def notifyAddedEvent(instance, event):
    logger.info(u"superclass.objcollect.notifyAddedEvent: event: %s" % event)
    import pdb
    pdb.set_trace()
    raw_instance = removeSecurityProxy(instance)
    iid = zapi.getUtility(IIntIds, '')
    iid.register(raw_instance)
    connection = IConnection(raw_instance)
    oc = connection.root()['_oq_collection']
    oc.index(raw_instance)


@adapter(ISuperclass, IObjectRemovedEvent)
def notifyRemovedEvent(instance, event):
    logger.info(u"superclass.objcollect.notifyRemovedEvent: event: %s" % event)
    raw_instance = removeSecurityProxy(instance)
    connection = IConnection(raw_instance)
    oc = connection.root()['_oq_collection']
    oc.unindex(raw_instance)


@adapter(ISuperclass, IObjectModifiedEvent)
def notifyModifiedEvent(instance, event):
    logger.info(u"superclass.objcollect.notifyModifiedEvent: event: %s" % event)
    raw_instance = removeSecurityProxy(instance)
    connection = IConnection(raw_instance)
    oc = connection.root()['_oq_collection']
    oc.index(raw_instance)
