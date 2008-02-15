# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611,W0612,W0613
#
"""startup of subsystem"""

__version__ = "$Id$"

# phython imports
import logging

# zope imports
from zope.component import adapter, queryUtility
from zope.app.zapi import getPath
from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.container.interfaces import IObjectModifiedEvent
from zope.app.container.interfaces import IObjectMovedEvent
from zope.app.container.interfaces import IObjectRemovedEvent

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import IPickle
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjMQ

logger = logging.getLogger("Compon. Supernode")


@adapter(ISupernode, IObjectAddedEvent)
def notifyAddedEvent(instance, event):
    """
    Node was added
    """
    #logger.info(u"supernode.objmq.notifyAddedEvent: event: %s" % event)
    supervisor = queryUtility(IAdmUtilSupervisor)
    if supervisor and supervisor.isSlave():
        if hasattr(event.object, "getObjectId"):
            objectOid = event.object.getObjectId()
        else:
            objectOid = None
        if hasattr(event.oldParent, "getObjectId"):
            oldParentOid = event.oldParent.getObjectId()
        else:
            oldParentOid = None
        if hasattr(event.newParent, "getObjectId"):
            newParentOid = event.newParent.getObjectId()
        else:
            newParentOid = None
        mq_utility = queryUtility(IAdmUtilObjMQ)
        recPickle = IPickle(event.object)
        if mq_utility and supervisor and recPickle:
            my_data = {'cmd': 'obj_added',
                       'oldparent': oldParentOid,
                       'newparent': newParentOid,
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

@adapter(ISupernode, IObjectModifiedEvent)
def notifyModifiedEvent(instance, event):
    """
    Node was modified
    """
    #logger.info(u"supernode.objmq.notifyModifiedEvent: event: %s" % event)
    for i in event.descriptions:
        logger.info(u"descr: %s" %i)
        logger.info(u"descr.interface: %s" % str(i.interface))
        for j in i.attributes:
            logger.info(u"    attribute / j: %s" % j)
            logger.info(u"    attribute / type(j): %s" % (type(j)))
    if hasattr(event.object, "getObjectId"):
        objectOid = event.object.getObjectId()
    else:
        objectOid = None
    #print "objectOid: %s" % objectOid
    mq_utility = queryUtility(IAdmUtilObjMQ)
    #print "mq_utility: %s" % mq_utility
    sv_utility = queryUtility(IAdmUtilSupervisor, context=instance)
    #print "sv_utility: %s" % sv_utility
    #print "sv_utility.objectID: %s" % sv_utility.objectID

@adapter(ISupernode, IObjectRemovedEvent)
def notifyRemovedEvent(instance, event):
    """
    Node was removed
    """
    #logger.info(u"supernode.objmq.notifyRemovedEvent: event: %s" % event)
    supervisor = queryUtility(IAdmUtilSupervisor, context=instance)
    if supervisor and supervisor.isSlave():
        if hasattr(event.object, "getObjectId"):
            objectOid = event.object.getObjectId()
        else:
            objectOid = None
        if hasattr(event.oldParent, "getObjectId"):
            oldParentOid = event.oldParent.getObjectId()
        else:
            oldParentOid = None
        if hasattr(event.newParent, "getObjectId"):
            newParentOid = event.newParent.getObjectId()
        else:
            newParentOid = None
        mq_utility = queryUtility(IAdmUtilObjMQ)
        if mq_utility and supervisor:
            my_data = {'cmd': 'obj_removed',
                       'oldparent': oldParentOid,
                       'newparent': newParentOid,
                       'objectOid': objectOid}
            my_data['header'] = {'from_oid': supervisor.objectID,
                                 'from_ip': supervisor.ipv4My,
                                 'from_path': getPath(supervisor),
                                 'to_oid': supervisor.oidMaster,
                                 'to_ip': supervisor.ipv4Master,
                                 'to_path': u"/++etc++site/default"+\
                                 "/AdmUtilSupervisor"
                             }
            mq_utility.sendPerMq(my_data)

@adapter(ISupernode, IObjectMovedEvent)
def notifyMovedEvent(instance, event):
    """
    Node was moved
    """
    #logger.info(u"supernode.objmq.notifyMovedEvent: event: %s" % event)
    supervisor = queryUtility(IAdmUtilSupervisor, context=instance)
    if supervisor and supervisor.isSlave():
        if hasattr(event.object, "getObjectId"):
            objectOid = event.object.getObjectId()
        else:
            objectOid = None
        if hasattr(event.oldParent, "getObjectId"):
            oldParentOid = event.oldParent.getObjectId()
        else:
            oldParentOid = None
        if hasattr(event.newParent, "getObjectId"):
            newParentOid = event.newParent.getObjectId()
        else:
            newParentOid = None
        mq_utility = queryUtility(IAdmUtilObjMQ)
        if mq_utility and supervisor:
            my_data = {'cmd': 'obj_moved',
                       'oldparent': oldParentOid,
                       'newparent': newParentOid,
                       'objectOid': objectOid}
            my_data['header'] = {'from_oid': supervisor.objectID,
                                 'from_ip': supervisor.ipv4My,
                                 'from_path': getPath(supervisor),
                                 'to_oid': supervisor.oidMaster,
                                 'to_ip': supervisor.ipv4Master,
                                 'to_path': u"/++etc++site/default"+\
                                 "/AdmUtilSupervisor"
                             }
            mq_utility.sendPerMq(my_data)
