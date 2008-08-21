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

# phython imports
import logging

# zope imports
from zope.component import adapter, queryUtility
from zope.app.zapi import getPath
from zope.lifecycleevent.interfaces import IObjectCopiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.app.container.interfaces import IObjectRemovedEvent

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import IPickle, \
     ISuperclass
from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjMQ
#from org.ict_ok.components.superclass.interfaces import IPickle
#from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
#from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjMQ

logger = logging.getLogger("Compon. Superclass")


@adapter(ISuperclass, IObjectCopiedEvent)
def notifyCopiedEvent(instance, event):
    #logger.info(u"superclass.objmq.notifyCopiedEvent: event: %s" % event)
    if hasattr(event.object, "getObjectId"):
        objectOid = event.object.getObjectId()
    else:
        objectOid = None
    #print "objectOid: %s" % objectOid
    if hasattr(event.original, "getObjectId"):
        originalOid = event.original.getObjectId()
    else:
        originalOid = None
    #print "originalOid: %s" % originalOid
    mq_utility = queryUtility(IAdmUtilObjMQ)
    #print "mq_utility: %s" % mq_utility
    

@adapter(ISuperclass, IObjectCreatedEvent)
def notifyCreatedEvent(instance, event):
    logger.info(u"superclass.objmq.notifyCreatedEvent: event: %s" % event)
    if hasattr(event.object, "getObjectId"):
        objectOid = event.object.getObjectId()
    else:
        objectOid = None
    #print "objectOid: %s" % objectOid
    mq_utility = queryUtility(IAdmUtilObjMQ)
    #print "mq_utility: %s" % mq_utility

@adapter(ISuperclass, IObjectRemovedEvent)
def notifyRemovedEvent(instance, event):
    logger.info(u"superclass.objmq.notifyRemovedEvent: event: %s" % event)
    if hasattr(event.object, "getObjectId"):
        objectOid = event.object.getObjectId()
    else:
        objectOid = None
    #print "objectOid: %s" % objectOid
    #mq_utility = queryUtility(IAdmUtilObjMQ)
    #print "mq_utility: %s" % mq_utility



@adapter(ISuperclass, IObjectModifiedEvent)
def notifyModifiedEvent(instance, event):
    supervisor = queryUtility(IAdmUtilSupervisor, context=instance)
    if supervisor and supervisor.isSlave():
        if hasattr(event.object, "getObjectId"):
            objectOid = event.object.getObjectId()
        else:
            objectOid = None
        mq_utility = queryUtility(IAdmUtilObjMQ)
        recPickle = IPickle(event.object)
        if mq_utility and supervisor and recPickle:
            my_data = {'cmd': 'obj_modified',
                       'obj': recPickle.exportAsDict()}
            my_data['header'] = {'from_oid': supervisor.objectID,
                                 'from_ip': supervisor.ipv4My,
                                 'from_path': getPath(supervisor),
                                 'to_oid': supervisor.oidMaster,
                                 'to_ip': supervisor.ipv4Master,
                                 'to_path': u"/++etc++site/default"+\
                                 "/AdmUtilSupervisor"
                             }
            mq_utility.sendPerMq(my_data)

