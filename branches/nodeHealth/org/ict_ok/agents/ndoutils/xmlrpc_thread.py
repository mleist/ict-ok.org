# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=
#
"""
xmlrpc-thread for ndo-agent for IKOMtrol
"""

__version__ = "$Id$"
__versRevision = "$LastChangedRevision$"

# phython imports
import time
import threading
import socket
import httplib
from base64 import encodestring
import xmlrpclib

# ict_ok.org imports
from org.ict_ok.libs.iklogger import IkLogger
from org.ict_ok.version import getVersRevision


class BasicAuthTransport(xmlrpclib.Transport):
    def __init__(self, arg_username=None,
                 arg_password=None, arg_verbose=0):
        self.username = arg_username
        self.password = arg_password
        self.verbose = arg_verbose
        self._use_datetime = 0 # Needed for Python 2.5 `Transport`

    def request(self, arg_host, handler,
                request_body, verbose=0):
        # issue XML-RPC request

        self.verbose = verbose

        myHttp = httplib.HTTP(arg_host)
        myHttp.putrequest("POST", handler)

        # required by HTTP/1.1
        myHttp.putheader("Host", arg_host)

        # required by XML-RPC
        myHttp.putheader("User-Agent", self.user_agent)
        myHttp.putheader("Content-Type", "text/xml")
        myHttp.putheader("Content-Length", str(len(request_body)))

        # basic auth
        if self.username is not None and self.password is not None:
            myHttp.putheader("AUTHORIZATION", "Basic %s" %
                             encodestring("%s:%s" % (self.username, self.password)
                                          ).replace("\012", ""))
        myHttp.endheaders()

        if request_body:
            myHttp.send(request_body)

        errcode, errmsg, headers = myHttp.getreply()

        if errcode != 200:
            raise xmlrpclib.ProtocolError(arg_host + handler,
                                          errcode, errmsg, headers)

        return self.parse_response(myHttp.getfile())


class XmlRpcThread(threading.Thread):
    def __init__(self, pQueue):
        self.logger = IkLogger("ik_ndoutils:IkTransfThread")
        self.logger.log.info("IKOMtrol NDO-XML-RPC Thread (Rev.: %s)" % \
                             getVersRevision(\
                                 "$LastChangedRevision$") )
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        self.pQueue = pQueue
        self.username = 'admin'
        self.password = 'admin'
        #self.url = 'http://localhost:8080/++etc++site/default/IkAdmUtilGeneratorNagios'
        self.url = "http://localhost:8081/++etc++site/default/AdmUtilGeneratorNagios"
        self.host = xmlrpclib.Server(self.url, transport = \
                                     BasicAuthTransport(self.username,
                                                        self.password))
        threading.Thread.__init__(self, name="IkTransfThread")

    def run(self):
        """
        overload of threading.thread.run()
        main control loop
        """
        while not self._stopevent.isSet():
            while self.pQueue.qsize > 0:
                tmpObj = self.pQueue.get()
                errorFlag = False
                try:
                    print "2a"
                    self.host.ddd(1)
                    print "2b"
                    self.host.triggerNdoEvent(tmpObj)
                    print "2c"
                except socket.error, errText:
                    errorFlag = True
                    self.logger.log.error("Error in XML-RPC call: %s" % errText)
                    time.sleep(10)
                except Exception, errText:
                    errorFlag = True
                    self.logger.log.error("Error in XML-RPC call: %s" % errText)
                    time.sleep(10)
                # this will delete the Object from Queue
                if not errorFlag:
                    self.pQueue.get()
            self._stopevent.wait(self._sleepperiod)

    def join(self,timeout=None):
        """
        Stop the thread
        """
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        del self.logger

if __name__ == "__main__":
    print "don't do this"
