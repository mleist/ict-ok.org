# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0612
#
"""
ndo-thread for ndo-agent for IKOMtrol
"""

__version__ = "$Id$"
__versRevision = "$LastChangedRevision$"

# phython imports
import sys
import time
import re
import threading
import SocketServer
import signal
from socket import AF_UNIX, SOCK_STREAM, socket

# zope imports

# ict_ok.org imports
from org.ict_ok.libs.iklogger import IkLogger
from org.ict_ok.libs.ikqueue import IkQueue
from org.ict_ok.version import getVersRevision

ndo_data_types = {
    "100": "NDO_API_LOGENTRY",
    "200": "NDO_API_PROCESSDATA",
    "201": "NDO_API_TIMEDEVENTDATA",
    "202": "NDO_API_LOGDATA",
    "203": "NDO_API_SYSTEMCOMMANDDATA",
    "204": "NDO_API_EVENTHANDLERDATA",
    "205": "NDO_API_NOTIFICATIONDATA",
    "206": "NDO_API_SERVICECHECKDATA",
    "207": "NDO_API_HOSTCHECKDATA",
    "208": "NDO_API_COMMENTDATA",
    "209": "NDO_API_DOWNTIMEDATA",
    "210": "NDO_API_FLAPPINGDATA",
    "211": "NDO_API_PROGRAMSTATUSDATA",
    "212": "NDO_API_HOSTSTATUSDATA",
    "213": "NDO_API_SERVICESTATUSDATA",
    "214": "NDO_API_ADAPTIVEPROGRAMDATA",
    "215": "NDO_API_ADAPTIVEHOSTDATA",
    "216": "NDO_API_ADAPTIVESERVICEDATA",
    "217": "NDO_API_EXTERNALCOMMANDDATA",
    "218": "NDO_API_AGGREGATEDSTATUSDATA",
    "219": "NDO_API_RETENTIONDATA",
    "220": "NDO_API_CONTACTNOTIFICATIONDATA",
    "221": "NDO_API_CONTACTNOTIFICATIONMETHODDATA",
    "222": "NDO_API_ACKNOWLEDGEMENTDATA",
    "223": "NDO_API_STATECHANGEDATA",
    "224": "NDO_API_CONTACTSTATUSDATA",
    "225": "NDO_API_ADAPTIVECONTACTDATA",
    "300": "NDO_API_MAINCONFIGFILEVARIABLES",
    "301": "NDO_API_RESOURCECONFIGFILEVARIABLES",
    "302": "NDO_API_CONFIGVARIABLES",
    "303": "NDO_API_RUNTIMEVARIABLES",
    "400": "NDO_API_HOSTDEFINITION",
    "401": "NDO_API_HOSTGROUPDEFINITION",
    "402": "NDO_API_SERVICEDEFINITION",
    "403": "NDO_API_SERVICEGROUPDEFINITION",
    "404": "NDO_API_HOSTDEPENDENCYDEFINITION",
    "405": "NDO_API_SERVICEDEPENDENCYDEFINITION",
    "406": "NDO_API_HOSTESCALATIONDEFINITION",
    "407": "NDO_API_SERVICEESCALATIONDEFINITION",
    "408": "NDO_API_COMMANDDEFINITION",
    "409": "NDO_API_TIMEPERIODDEFINITION",
    "410": "NDO_API_CONTACTDEFINITION",
    "411": "NDO_API_CONTACTGROUPDEFINITION",
    "412": "NDO_API_HOSTEXTINFODEFINITION",
    "413": "NDO_API_SERVICEEXTINFODEFINITION",
}


class MyHandler(SocketServer.StreamRequestHandler):
    def cmd_out(self, pQueue, cmd):
        if cmd['99999'] in ['201', '218', '211']:
            return
        #if ndo_data_types.has_key(cmd['99999']):
            #self.server.threadLogger.log.info("put cmd (%s) into queue" % \
                                               #ndo_data_types[cmd['99999']])
        #self.server.threadLogger.log.debug("data: [%s]" % \
                                           #str(cmd))
        self.server.packageCounter += 1
        cmd['99997'] = self.server.packageCounter
        pQueue.put(cmd)

    def handle(self):
        while True:
            #line = self.rfile.readline()
            #self.server.threadLogger.log.info("->%s" % line)
            #print "(%s)-> %s" % (self.server, line)
            #self.server.threadLogger.log.info("->%s" % self.rfile.readlines())
            data = self.request.recv(65536)
            if len(data) > 0:
                #self.server.threadLogger.log.info("->%s" % data)
                stringList = data.split("\n")
                while stringList.count("") >0:
                    del stringList[stringList.index("")]
                for n, i in enumerate(stringList):
                    re_start = re.match("^(\d*):$", i)
                    if re_start:
                        cmd={}
                        cmd['99999'] = re_start.group(1).strip()
                        #print "------------ START (%s) -------------" % (re_start.group(1).strip())
                    re_arg = re.match("^(\d*)=(.*)$", i)
                    if re_arg:
                        #print "Arg->   [%s] = [%s]" % (re_arg.group(1).strip(), re_arg.group(2).strip())
                        cmd[str(re_arg.group(1).strip())]=re_arg.group(2).strip()
                    #print"i: %s (%s, %s)" % (i, len(i), n)
                    re_end = re.match("^999$", i)
                    if re_end:
                        #print "------------ STOP ----------------"
                        self.cmd_out(self.server.pQueue, cmd)
            else:
                time.sleep(1)


class IkNdoServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    special IKOMtrol XMLRPC-Server, secure https
    """
    def __init__(self, server_address, RequestHandlerClass,
                 pQueue, threadLogger):
        self.pQueue = pQueue
        self.threadLogger = threadLogger
        self.packageCounter = 0
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)


class NdoThread(threading.Thread):
    def __init__(self, pQueue):
        self.logger = IkLogger("ik_ndoutils:NdoThread")
        self.logger.log.info("IKOMtrol NDO Thread (Rev.: %s)" % \
                             getVersRevision(\
                                 "$LastChangedRevision$") )
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        #self.ndo_socket = socket(AF_UNIX, SOCK_STREAM)
        #self.ndo_socket.setblocking(0)
        #self.ndo_socket.bind('/opt/nagios/var/ndo.sock')
        self.tcpserver = IkNdoServer(('localhost', 15678),
                                     MyHandler, pQueue, self.logger)
        threading.Thread.__init__(self, name="NdoThread")
        
    def run(self):
        """
        overload of threading.thread.run()
        main control loop
        """
        while not self._stopevent.isSet():
            self.logger.log.info("starting NdoServer")
            #self.ndo_socket.listen(1)
            #self.conn, self.addr = self.ndo_socket.accept()
            self.tcpserver.handle_request()
            self.logger.log.info("ddd")
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
    