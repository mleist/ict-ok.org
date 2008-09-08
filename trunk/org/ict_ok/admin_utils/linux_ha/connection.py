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

# python imports
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
from org.ict_ok.admin_utils.linux_ha.hb_mini import miniManager
from org.ict_ok.admin_utils.linux_ha.classes import Cluster, Node, Ressource

logger = logging.getLogger("AdmUtilLinuxHa")
_ = MessageFactory('org.ict_ok')


class LinuxHaConnectionThread(threading.Thread):

    database = None
    __stopped = False

    def __init__(self):
        print "LinuxHaConnectionThread started"
        self.globalLinuxHa = None
        self.queues = {}
        self.clusters = {}
        self.miniManagers = {}
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
            #print "executeMyQueue"
            myParams = self.getQueue(utilOId)['in'].get(True, 15)
            #print "cmd: ", myParams['cmd']
            #sourceAdmUtilEsxVim = myParams['admUtilEsxVim']
            #sourceOId = sourceAdmUtilEsxVim.getObjectId()
            
            # make connection in worker thread
            if myParams.has_key('cmd'):
                if myParams['cmd'] == 'make_con':
                    print "jetzt die Verbindung bauen"
                    print "ip: ", myParams['conn_params']['ip']
                    print "port: ", myParams['conn_params']['port']
                    print "user: ", myParams['conn_params']['username']
                    print "passwd: ", myParams['conn_params']['password']
                    print "und los"
                    # eigentliche conn aufbauen ...
                    self.miniManagers[utilOId] = miniManager()
                    self.clusters[utilOId] = Cluster(\
                        "%s:%d" % (myParams['conn_params']['ip'],
                                   myParams['conn_params']['port']),
                        str(myParams['conn_params']['username']),
                        str(myParams['conn_params']['password']),
                        str(utilOId),
                        self.miniManagers[utilOId])
                    retCon = self.miniManagers[utilOId].login(\
                        str(self.clusters[utilOId].ip),
                        str(self.clusters[utilOId].user),
                        str(self.clusters[utilOId].passwd))
                    self.getQueue(utilOId)['out'].put(retCon, True, 15)
                elif myParams['cmd'] == 'get_nodes':
                    print "jetzt die knoten suchen"
                    objList = self.clusters[utilOId].getNodes()
                    retList = [obj.name for obj in objList]
                    self.getQueue(utilOId)['out'].put(retList, True, 15)
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
                        if myAdmUtilLinuxHa.linuxHaServerActive:
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
            #self.esx_logout(myAdmUtilLinuxHa)
            for minim_obj in self.miniManagers.values():
                minim_obj.logout()
            #setSite(old_site)
            transaction.commit()
            conn.close()

    def stop(self):
        LinuxHaConnectionThread.__stopped = True
        print "LinuxHaConnectionThread stopped"
        