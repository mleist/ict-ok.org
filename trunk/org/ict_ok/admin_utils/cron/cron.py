# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
#
"""implementation of a "cron daemon" 
"""

__version__ = "$Id$"

# phython imports
import logging
from datetime import datetime

# zope imports
from zope.interface import implements
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.dublincore.interfaces import IWriteZopeDublinCore

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.cron.interfaces import IAdmUtilCron
from org.ict_ok.admin_utils.cron.interfaces import IGlobalCronUtility

logger = logging.getLogger("AdmUtilCron")


class AdmUtilCron(Supernode):
    """Implementation of local Cron Utility"""

    implements(IAdmUtilCron)

    lastCron = "no signal since start"

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__

    def receiveCron(self, request, str_time, mode=None):
        """receive cron signal
        """
        #logger.info(u"AdmUtilCron::receiveCron(%s, %s) in '%s'" \
                    #% (str_time, mode,zapi.getPath(self)))
        self.lastCron = str_time
        dcore = IWriteZopeDublinCore(self)
        dcore.modified = datetime.utcnow()

    def getCronTime(self):
        """get last cron timestamp
        """
        try:
            retVal = self.lastCron
        except NameError:
            self.__setattr__("lastCron", "not set")
            retVal = self.lastCron
        return retVal


class GlobalCronUtility(object):
    """ Class for singleton utility
    """

    implements(IGlobalCronUtility)

    lastCron = "no signal since start"

    def __init__(self):
        #logger.info(u"GlobalCronUtility started")
        self.subscriber_list = []
        super(GlobalCronUtility, self).__init__(self)

    def subscribeToCron(self, obj):
        #logger.info(u"GlobalCronUtility::subscribe2cron(%s)" % obj)
        if obj not in self.subscriber_list:
            self.subscriber_list.append(obj)

    def unsubscribeFromCron(self, obj):
        #logger.info(u"GlobalCronUtility::unsubscribeFromCron(%s)" % obj)
        if obj in self.subscriber_list:
            self.subscriber_list.remove(obj)

    def receiveCron(self, request, str_time, str_mode=None):
        mode = None
        if str_mode.lower() in ['minute', 'hour', 'day',
                                'month', 'year', 'db_pack', 'db_pack_0']:
            mode = str_mode.lower()
        #logger.info(u"GlobalCronUtility::receiveCron (mode:%s)" % mode)
        if mode == 'db_pack':
            size_pre = request.publication.db.getSize()
            request.publication.db.pack(days=5)
            size_post = request.publication.db.getSize()
            logger.info(u"GlobalCronUtility / zodb packed %d -> %d" % \
                        (size_pre, size_post))
        if mode == 'db_pack_0':
            size_pre = request.publication.db.getSize()
            request.publication.db.pack(days=0)
            size_post = request.publication.db.getSize()
            logger.info(u"GlobalCronUtility / zodb packed %d -> %d" % \
                        (size_pre, size_post))
        for obj in self.subscriber_list:
            obj.receiveCron(request, str_time, mode)

    def getCronTime(self):
        try:
            retVal = self.lastCron
        except NameError:
            self.__setattr__("lastCron", "not set")
            retVal = self.lastCron
        return retVal


class AdmUtilCronRpcMethods(MethodPublisher):
    def isUp(self):
        """reachable check on the XMLRPC-Interface"""
        logger.info(u"AdmUtilCronRpcMethods::isUp (%s)" % self.__name__)
        return True

    def triggerCronEvent(self, str_time, str_mode):
        print "AdmUtilCronRpcMethods.triggerCronEvent(%s, %s)" % \
              (str_time, str_mode)
        from zope.proxy import removeAllProxies
        obj = removeAllProxies(self.context)
        obj.__setattr__("lastCron", str_time)
        globalCronUtility.receiveCron(self.request, str_time, str_mode)
        
globalCronUtility = GlobalCronUtility()
