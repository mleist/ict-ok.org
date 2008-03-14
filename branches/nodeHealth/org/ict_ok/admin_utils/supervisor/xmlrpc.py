# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""XML-RPC methods for Object Message Queue"""

__version__ = "$Id$"

# phython imports
import logging

# zope imports
from zope.app import zapi
from zope.app.publisher.xmlrpc import XMLRPCView
from zope.app.catalog.interfaces import ICatalog
from zope.xmlpickle import loads
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')

logger = logging.getLogger("AdmUtilSupervisor.XMLRPC")


class RpcMethods(XMLRPCView):
    """XML-RPC methods for Object Message Queue"""

    def objmq_subscribe(self, data):
        """inject obj from mq."""
        #logger.info(u"inject obj from mq. data:%s" % data)
        # cut first line with message id
        python_pickle = loads(data[1 + data.find("\n"):])
        my_catalog = zapi.getUtility(ICatalog)
        if python_pickle['cmd'].lower() == "connect":
            if self.context.objectID == \
               python_pickle['header']['to_oid']:
                self.context.appendSlave(\
                    python_pickle['header'],
                    python_pickle['nodename'])
                return u"connected"
            else:
                return u"unknown system"
        elif python_pickle['cmd'].lower() == "connected":
            if self.context.objectID == \
               python_pickle['header']['to_oid']:
                self.context.status2Master = u"connected"
                #self.context.lastSeenMaster = datetime.now(berlinTZ)
            else:
                return u"unknown system"
        elif python_pickle['cmd'].lower() == "ping":
            if self.context.objectID == \
               python_pickle['header']['to_oid']:
                #self.context.sendPong(python_pickle['header'])
                self.context.receivedPing(python_pickle['header'])
                #self.context.lastSeenMaster = datetime.now(berlinTZ)
            else:
                return u"unknown system"
        elif python_pickle['cmd'].lower() == "pong":
            if self.context.objectID == \
               python_pickle['header']['to_oid']:
                #self.context.lastSeenMaster = datetime.now(berlinTZ)
                self.context.receivedPong(python_pickle['header'])
            else:
                return u"unknown system"
        elif python_pickle['cmd'].lower() == "obj_added":
            if self.context.objectID == \
               python_pickle['header']['to_oid']:
                #self.context.lastSeenMaster = datetime.now(berlinTZ)
                self.context.addObject(python_pickle['header'],
                                       python_pickle['oldparent'],
                                       python_pickle['newparent'],
                                       python_pickle['obj'])
            else:
                return u"unknown system"
        elif python_pickle['cmd'].lower() == "obj_removed":
            if self.context.objectID == \
               python_pickle['header']['to_oid']:
                #self.context.lastSeenMaster = datetime.now(berlinTZ)
                self.context.removeObject(python_pickle['header'],
                                          python_pickle['oldparent'],
                                          python_pickle['newparent'],
                                          python_pickle['objectOid'])
            else:
                return u"unknown system"
        elif python_pickle['cmd'].lower() == "obj_modified":
            if self.context.objectID == \
               python_pickle['header']['to_oid']:
                #self.context.lastSeenMaster = datetime.now(berlinTZ)
                self.context.modifyObject(python_pickle['header'],
                                          python_pickle['obj'])
            else:
                return u"unknown system"
        elif python_pickle['cmd'].lower() == "obj_moved":
            if self.context.objectID == \
               python_pickle['header']['to_oid']:
                #self.context.lastSeenMaster = datetime.now(berlinTZ)
                self.context.moveObject(python_pickle['header'],
                                        python_pickle['oldparent'],
                                        python_pickle['newparent'],
                                        python_pickle['objectOid'])
            else:
                return u"unknown system"
        else:
            return u"unknown command"
        return u"permission denied"
  