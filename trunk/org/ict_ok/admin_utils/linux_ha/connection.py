# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""implementation of a "linux-ha connection thread" 
"""

__version__ = "$Id$"

# phython imports
import logging
import threading
import atexit
import time

# zope imports
import transaction
from zope.i18nmessageid import MessageFactory
from zope.app.component.hooks import getSite, setSite
from zope.component import queryUtility

# ict_ok.org imports
from org.ict_ok.libs.ikqueue import IkQueue
from org.ict_ok.admin_utils.linux_ha.interfaces import IAdmUtilLinuxHa

logger = logging.getLogger("AdmUtilLinuxHa")
_ = MessageFactory('org.ict_ok')


class LinuxHaConnectionThread(threading.Thread):

    database = None
    __stopped = False

    def __init__(self):
        print "LinuxHaConnectionThread started"
        self.globalLinuxHa = None
        self.queues = {}
        threading.Thread.__init__(self)

    def createQueue(self, queueId):
        if not self.queues.has_key(queueId):
            self.queues[queueId] = {\
                'in': IkQueue(),
                'out': IkQueue()}
            return self.queues[queueId]

    def getQueue(self, queueId):
        if self.queues.has_key(queueId):
            return (self.queues[queueId])
        else:
            return self.createQueue(queueId)

    def is_logged_in(self, myAdmUtilLinuxHa):
        if self.globalLinuxHa:
            if self.globalLinuxHa.connection_dict.has_key(\
                    myAdmUtilLinuxHa.getObjectId()):
                return True
        return False

    def del_logged_in(self, myAdmUtilLinuxHa):
        if self.globalLinuxHa:
            if self.globalLinuxHa.connection_dict.has_key(\
                    myAdmUtilLinuxHa.getObjectId()):
                del self.globalLinuxHa.connection_dict[\
                    myAdmUtilLinuxHa.getObjectId()]
                return True
        return False

    def hb_login(self, myAdmUtilLinuxHa):
        try:
            if self.globalLinuxHa:
                if self.is_logged_in(myAdmUtilLinuxHa):
                    pass
                else:
                    #print "login"
                    my_service_url = "https://%s:%s/sdk/webService" % \
                                   (myAdmUtilLinuxHa.hbVimServerIp,
                                    myAdmUtilLinuxHa.hbVimServerPort)
                    #print "service_url: ", my_service_url
                    retVal = self.perl.call("Vim::login",
                                            service_url = str(my_service_url),
                                            user_name = u"%s" % myAdmUtilLinuxHa.hbVimUsername,
                                            password = u"%s" % myAdmUtilLinuxHa.hbVimPassword
                                        )
                    self.globalLinuxHa.connection_dict[\
                        myAdmUtilLinuxHa.getObjectId()] = \
                        retVal
                    myAdmUtilLinuxHa.setConnStatus(u"connect ok")
                    tmpApiFullName = "%s" % retVal.about().fullName()
                    if myAdmUtilLinuxHa.apiFullName != tmpApiFullName:
                        myAdmUtilLinuxHa.apiFullName = tmpApiFullName
                    return True
        except self.perl.PerlError, err:
            errStringList = str(err).split('\n')
            myErrorText = errStringList[0] + '/' + errStringList[1]
            myAdmUtilLinuxHa.setConnStatus(u"connect error:" + myErrorText)
            self.del_logged_in(myAdmUtilLinuxHa)
            time.sleep(3)
        return False

    def hb_logout(self, myAdmUtilLinuxHa):
        print "hb_logout"
        if self.globalLinuxHa:
            if self.perl is not None:
                try:
                    print "Vim::logout"
                    retVal = self.perl.call("Vim::logout")
                    print "logged out, retVal:", retVal
                    return True
                except self.perl.PerlError, err:
                    errStringList = str(err).split('\n')
                    myErrorText = errStringList[0] + '/' + errStringList[1]
                    myAdmUtilLinuxHa.setConnStatus(u"connect error:" + myErrorText)
                    self.del_logged_in(myAdmUtilLinuxHa)
                    time.sleep(1)
        return False

    def getAllLinuxHaDatacenter(self, myAdmUtilLinuxHa):
        print "LinuxHaConnectionThread.getAllLinuxHaDatacenter"
        if self.globalLinuxHa:
            self.hb_login(myAdmUtilLinuxHa)
            try:
                if self.perl is not None:
                    datacenterList = self.perl.call("Vim::find_entity_views", view_type="Datacenter")
                    return datacenterList
            except self.perl.PerlError, err:
                errStringList = str(err).split('\n')
                myErrorText = errStringList[0] + '/' + errStringList[1]
                myAdmUtilLinuxHa.setConnStatus(u"connect error:" + myErrorText)
                self.del_logged_in(myAdmUtilLinuxHa)
        return []

    def getAllLinuxHaEntityViews(self, myParams):
        #print "LinuxHaConnectionThread.getAllLinuxHaEntityViews(%s)" % myParams
        if self.globalLinuxHa:
            #print "77777a1"
            self.hb_login(myParams['admUtilLinuxHa'])
            #print "77777a2"
            try:
                if self.perl is not None:
                    if myParams['cmd'] == 'find_entity_views':
                        if myParams.has_key('filter'):
                            if myParams.has_key('begin_entity'):
                                retList = self.perl.call("Vim::find_entity_views", \
                                                         view_type=myParams['view_type'], \
                                                         begin_entity=myParams['begin_entity'], \
                                                         filter=myParams['filter'])
                            else:
                                retList = self.perl.call("Vim::find_entity_views", \
                                                         view_type=myParams['view_type'], \
                                                         filter=myParams['filter'])
                        else:
                            if myParams.has_key('begin_entity'):
                                retList = self.perl.call("Vim::find_entity_views", \
                                                         begin_entity=myParams['begin_entity'], \
                                                         view_type=myParams['view_type'])
                            else:
                                retList = self.perl.call("Vim::find_entity_views", \
                                                         view_type=myParams['view_type'])
                        return retList
            except self.perl.PerlError, err:
                #print "77777: ", err
                errStringList = str(err).split('\n')
                myErrorText = errStringList[0] + '/' + errStringList[1]
                if myParams.has_key('admUtilLinuxHa') and \
                   myParams['admUtilLinuxHa'] is not None:
                    myParams['admUtilLinuxHa'].setConnStatus(u"connect error:" + myErrorText)
                    self.del_logged_in(myParams['admUtilLinuxHa'])
        return []
    
    def executeMyQueue(self, myAdmUtilLinuxHa):
        utilOId = myAdmUtilLinuxHa.getObjectId()
        if not self.getQueue(utilOId)['in'].empty():
            print "executeMyQueue"
            myParams = self.getQueue(utilOId)['in'].get(True, 15)
            print "cmd: ", myParams['cmd']
            sourceAdmUtilLinuxHa = myParams['admUtilLinuxHa']
            sourceOId = sourceAdmUtilLinuxHa.getObjectId()
            self.getQueue(sourceOId)['out'].put(None, True, 15)
            self.getQueue(utilOId)['in'].task_done()

    def run(self, forever=True):
        atexit.register(self.stop)
        while not self.__stopped:
            if LinuxHaConnectionThread.database:
                try:
                    conn = LinuxHaConnectionThread.database.open()
                    root = conn.root()
                    root_folder = root['Application']
                    old_site = getSite()
                    setSite(root_folder)
                    myAdmUtilLinuxHa = queryUtility(IAdmUtilLinuxHa)
                    if myAdmUtilLinuxHa is not None:
                        utilOId = myAdmUtilLinuxHa.getObjectId()
                        if myAdmUtilLinuxHa.esxVimServerActive:
                            if not self.is_logged_in(myAdmUtilLinuxHa):
                                if not self.perl_imports():
                                    logger.error("Perl Error: imports")
                                    raise Exception, "Perl Error: imports"
                                if not self.esx_login(myAdmUtilLinuxHa):
                                    logger.info("ESX Vim Error on login()")
                            self.executeMyQueue(myAdmUtilLinuxHa)
                        else:
                            if not self.getQueue(utilOId)['in'].empty():
                                self.getQueue(utilOId)['in'].get(True, 5)
                                self.getQueue(utilOId)['in'].task_done()
                    transaction.commit()
                    conn.close()
                    # Blanket except because we don't want
                    # this thread to ever die
                except Exception, err:
                    logger.error("Error in ESX VIM (%s)" % err, exc_info=True)
                    transaction.abort()
                    conn.close()
#--------------------------------------------------------------------------------
            if forever:
                time.sleep(0.01)
            else:
                break
        if LinuxHaConnectionThread.database:
            conn = LinuxHaConnectionThread.database.open()
            root = conn.root()
            root_folder = root['Application']
            old_site = getSite()
            setSite(root_folder)
            myAdmUtilLinuxHa = queryUtility(IAdmUtilLinuxHa)
            self.esx_logout(myAdmUtilLinuxHa)
            #setSite(old_site)
            transaction.commit()
            conn.close()

    def stop(self):
        LinuxHaConnectionThread.__stopped = True
        print "LinuxHaConnectionThread stopped"
        