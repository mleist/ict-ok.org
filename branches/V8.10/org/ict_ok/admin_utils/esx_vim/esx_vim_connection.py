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
"""implementation of an "esx_vim connection thread" 
"""

#TODO delete debug statements

__version__ = "$Id$"

# python imports
import logging
import threading
import atexit
import perl
import time

# zope imports
import transaction
from zope.i18nmessageid import MessageFactory
from zope.app.component.hooks import getSite, setSite
from zope.component import queryUtility

# ict_ok.org imports
from org.ict_ok.libs.ikqueue import IkQueue
from org.ict_ok.admin_utils.esx_vim.interfaces import IAdmUtilEsxVim

logger = logging.getLogger("AdmUtilEsxVim")
_ = MessageFactory('org.ict_ok')


class EsxVimConnectionThread(threading.Thread):

    database = None
    __stopped = False

    def __init__(self):
        print "EsxVimConnectionThread started"
        self.globalEsxVim = None
        self.perl = None
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

    def perl_imports(self):
        self.perl = perl
        try:
            self.perl.require("VMware::VIM2Runtime")
        except self.perl.PerlError, err:
            print "My Perl Error: ", err
            time.sleep(1)
            return False
        try:
            self.perl.require("VMware::VILib")
        except self.perl.PerlError, err:
            print "My Perl Error: ", err
            time.sleep(1)
            return False
        return True

    def is_logged_in(self, myAdmUtilEsxVim):
        if self.globalEsxVim:
            if self.globalEsxVim.connection_dict.has_key(\
                    myAdmUtilEsxVim.getObjectId()):
                return True
        return False

    def del_logged_in(self, myAdmUtilEsxVim):
        if self.globalEsxVim:
            if self.globalEsxVim.connection_dict.has_key(\
                    myAdmUtilEsxVim.getObjectId()):
                del self.globalEsxVim.connection_dict[\
                    myAdmUtilEsxVim.getObjectId()]
                return True
        return False

    def esx_login(self, myAdmUtilEsxVim):
        try:
            if self.globalEsxVim:
                if self.is_logged_in(myAdmUtilEsxVim):
                    # logout machen ?
                    pass
                else:
                    #print "Vim::login"
                    my_service_url = "https://%s:%s/sdk/webService" % \
                                   (myAdmUtilEsxVim.esxVimServerIp,
                                    myAdmUtilEsxVim.esxVimServerPort)
                    #print "service_url: ", my_service_url
                    retVal = self.perl.call("Vim::login",
                                            service_url = str(my_service_url),
                                            user_name = u"%s" % myAdmUtilEsxVim.esxVimUsername,
                                            password = u"%s" % myAdmUtilEsxVim.esxVimPassword
                                        )
                    self.globalEsxVim.connection_dict[\
                        myAdmUtilEsxVim.getObjectId()] = \
                        retVal
                    myAdmUtilEsxVim.setConnStatus(u"connect ok")
                    tmpApiFullName = "%s" % retVal.about().fullName()
                    if myAdmUtilEsxVim.apiFullName != tmpApiFullName:
                        myAdmUtilEsxVim.apiFullName = tmpApiFullName
                    return True
        except self.perl.PerlError, err:
            errStringList = str(err).split('\n')
            myErrorText = errStringList[0] + '/' + errStringList[1]
            myAdmUtilEsxVim.setConnStatus(u"connect error:" + myErrorText)
            self.del_logged_in(myAdmUtilEsxVim)
            time.sleep(3)
        return False

    def esx_logout(self, myAdmUtilEsxVim):
        print "esx_logout"
        if self.globalEsxVim:
            if self.perl is not None:
                try:
                    print "Vim::logout"
                    retVal = self.perl.call("Vim::logout")
                    print "logged out, retVal:", retVal
                    return True
                except self.perl.PerlError, err:
                    errStringList = str(err).split('\n')
                    myErrorText = errStringList[0] + '/' + errStringList[1]
                    myAdmUtilEsxVim.setConnStatus(u"connect error:" + myErrorText)
                    self.del_logged_in(myAdmUtilEsxVim)
                    time.sleep(1)
        return False

    def getAllEsxVimDatacenter(self, myAdmUtilEsxVim):
        print "EsxVimConnectionThread.getAllEsxVimDatacenter"
        if self.globalEsxVim:
            self.esx_login(myAdmUtilEsxVim)
            try:
                if self.perl is not None:
                    datacenterList = self.perl.call("Vim::find_entity_views", view_type="Datacenter")
                    return datacenterList
            except self.perl.PerlError, err:
                errStringList = str(err).split('\n')
                myErrorText = errStringList[0] + '/' + errStringList[1]
                myAdmUtilEsxVim.setConnStatus(u"connect error:" + myErrorText)
                self.del_logged_in(myAdmUtilEsxVim)
        return []

    def getAllEsxVimEntityViews(self, myParams):
        #print "EsxVimConnectionThread.getAllEsxVimEntityViews(%s)" % myParams
        if self.globalEsxVim:
            #print "77777a1"
            self.esx_login(myParams['admUtilEsxVim'])
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
                if myParams.has_key('admUtilEsxVim') and \
                   myParams['admUtilEsxVim'] is not None:
                    myParams['admUtilEsxVim'].setConnStatus(u"connect error:" + myErrorText)
                    self.del_logged_in(myParams['admUtilEsxVim'])
        return []
    
    def executeMyQueue(self, myAdmUtilEsxVim):
        utilOId = myAdmUtilEsxVim.getObjectId()
        if not self.getQueue(utilOId)['in'].empty():
            #print "executeMyQueue"
            myParams = self.getQueue(utilOId)['in'].get(True, 15)
            #print "cmd: ", myParams['cmd']
            sourceAdmUtilEsxVim = myParams['admUtilEsxVim']
            sourceOId = sourceAdmUtilEsxVim.getObjectId()
            if myParams.has_key('cmd'):
                if myParams['cmd'] == 'find_entity_views':
                    esxObjList = self.getAllEsxVimEntityViews(myParams)
                    myList = []
                    for esxObj in esxObjList:
                        try:
                            tmpUuid = esxObj.config().uuid()
                        except Exception:
                            tmpUuid = None
                        myList.append({\
                            'name': u"%s" % (esxObj.name()),
                            'overallStatus': u"%s" % (esxObj.overallStatus().val()),
                            'uuid': tmpUuid,
                            'esxType': myParams['view_type'],
                            'perlRef': esxObj,
                        })
                    self.getQueue(sourceOId)['out'].put(myList, True, 15)
                elif myParams['cmd'] == 'call_fcnt_on_obj':
                    if myParams.has_key('perlRef') and \
                       myParams.has_key('fnct_name') and \
                       myParams.has_key('fnct_args') and \
                       type(myParams['fnct_name']) == type('') and \
                       type(myParams['fnct_args']) == type({}):
                        myObj = myParams['perlRef']
                        myFnctName = myParams['fnct_name']
                        myFnctArgs = myParams['fnct_args']
                        try:
                            retVal = getattr(myObj, myFnctName)(**myFnctArgs)
                            self.getQueue(sourceOId)['out'].put(retVal, True, 15)
                        except self.perl.PerlError, err:
                            print "My Perl Error: ", err
                            self.getQueue(sourceOId)['out'].put(None, True, 15)
                    else:
                        self.getQueue(sourceOId)['out'].put(None, True, 15)
                elif myParams['cmd'] == 'eval_on_obj':
                    if myParams.has_key('perlRef') and \
                       myParams.has_key('eval_text') and \
                       myParams.has_key('fnct_args') and \
                       type(myParams['eval_text']) == type('') and \
                       (type(myParams['fnct_args']) == type({}) or \
                        type(myParams['fnct_args']) == type(None)):
                        myObj = myParams['perlRef']
                        myEvalText = myParams['eval_text']
                        print "myEvalText:", myEvalText
                        myFnctArgs = myParams['fnct_args']
                        try:
                            if myFnctArgs is None:
                                retVal = eval(myEvalText, {\
                                    'obj':myObj,
                                    'perl':self.perl})
                            else:
                                retVal = eval(myEvalText, {\
                                    'obj':myObj,
                                    'perl':self.perl})(**myFnctArgs)
                        except Exception,err:
                            retVal = err
                        self.getQueue(sourceOId)['out'].put(retVal, True, 15)
                    else:
                        self.getQueue(sourceOId)['out'].put(None, True, 15)
                else: # unknown command cmd
                    self.getQueue(sourceOId)['out'].put(None, True, 15)
            self.getQueue(utilOId)['in'].task_done()

    def run(self, forever=True):
        atexit.register(self.stop)
        while not self.__stopped:
            if EsxVimConnectionThread.database:
                try:
                    conn = EsxVimConnectionThread.database.open()
                    root = conn.root()
                    root_folder = root['Application']
                    old_site = getSite()
                    setSite(root_folder)
                    myAdmUtilEsxVim = queryUtility(IAdmUtilEsxVim)
                    if myAdmUtilEsxVim is not None:
                        utilOId = myAdmUtilEsxVim.getObjectId()
                        if myAdmUtilEsxVim.esxVimServerActive:
                            if not self.is_logged_in(myAdmUtilEsxVim):
                                if not self.perl_imports():
                                    logger.error("Perl Error: imports")
                                    raise Exception, "Perl Error: imports"
                                if not self.esx_login(myAdmUtilEsxVim):
                                    logger.info("ESX Vim Error on login()")
                            self.executeMyQueue(myAdmUtilEsxVim)
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
        if EsxVimConnectionThread.database:
            conn = EsxVimConnectionThread.database.open()
            root = conn.root()
            root_folder = root['Application']
            old_site = getSite()
            setSite(root_folder)
            myAdmUtilEsxVim = queryUtility(IAdmUtilEsxVim)
            self.esx_logout(myAdmUtilEsxVim)
            #setSite(old_site)
            transaction.commit()
            conn.close()

    def stop(self):
        EsxVimConnectionThread.__stopped = True
        print "EsxVimConnectionThread stopped"
        