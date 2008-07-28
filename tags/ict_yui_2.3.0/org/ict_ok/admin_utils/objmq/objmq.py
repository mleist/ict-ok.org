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
"""implementation of a "Object-Message-Queue-Utility" 
"""

__version__ = "$Id$"

# phython imports
import logging
import pickle

# zope imports
from zope.interface import implements
from zope.component import getUtility, queryUtility
from zope.sendmail.interfaces import IMailDelivery
from zope.xmlpickle import toxml

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjMQ
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor

logger = logging.getLogger("AdmUtilObjMQ")


class AdmUtilObjMQ(Supernode):
    """Implementation of local Object-Message-Queue-Utility"""

    implements(IAdmUtilObjMQ)

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__

    def sendPerMq(self, send_data=None):
        """
        will send command via Message Queue to an other System
        """
        supervisor = queryUtility(IAdmUtilSupervisor)
        mq_utility = getUtility(IMailDelivery, 'ikObjTransportQueue')
        if (supervisor and mq_utility and send_data):
            from_adr = u"http://%s@%s:8080%s" % \
                     (send_data['header']['from_oid'], \
                      send_data['header']['from_ip'], \
                      send_data['header']['from_path'])
            to_adr = u"http://%s@%s:8080%s" % \
                     (send_data['header']['to_oid'], \
                      send_data['header']['to_ip'], \
                      send_data['header']['to_path'])
            python_pickle = pickle.dumps(send_data)
            mq_utility.send(from_adr, [to_adr], toxml(python_pickle))

    def switchFromTo(self, inHeader):
        """
        will 'invert' our header from->to an to->from
        """
        retDict = {}
        retDict['from_oid'] = inHeader['to_oid']
        retDict['from_ip'] = inHeader['to_ip']
        retDict['from_path'] = inHeader['to_path']
        retDict['to_oid'] = inHeader['from_oid']
        retDict['to_ip'] = inHeader['from_ip']
        retDict['to_path'] = inHeader['from_path']
        return retDict