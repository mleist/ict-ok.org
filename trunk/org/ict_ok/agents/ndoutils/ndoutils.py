# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=
#
"""
ndo-agent for ict-ok.org
"""

__version__ = "$Id$"
__versRevision = "$LastChangedRevision$"

# phython imports
import sys
import time

# zope imports

# ict_ok.org imports
from org.ict_ok.libs.iklogger import IkLogger
from org.ict_ok.libs.ikqueue import IkQueue
from org.ict_ok.version import getVersRevision
from org.ict_ok.agents.ndoutils.ndo_thread import NdoThread
from org.ict_ok.agents.ndoutils.xmlrpc_thread import XmlRpcThread

if __name__ == "__main__":
    main_logger = IkLogger("ndoutils")
    main_logger.log.info("Nagios ndoutils Connector (Rev.: %s)" % \
                         getVersRevision(__versRevision) )
    main_logger.log.debug("create Queue")
    pQueue = IkQueue(maxsize=1000)

    ndoThread = NdoThread(pQueue)
    ndoThread.setDaemon(True)
    ndoThread.start()
    
    transThread = XmlRpcThread(pQueue)
    transThread.setDaemon(True)
    transThread.start()

    while 1:
        try:
            time.sleep(600)
            main_logger.log.debug("600 sec trigger")
        except KeyboardInterrupt:
            main_logger.log.info("Interrupted by Keyboard")
            #pQueue.sync()
            #main_logger.log.info("Queue synced")
            sys.exit()
            break

    transThread.join()
    ndoThread.join()
    del pQueue
    main_logger.log.info("Logger stopped")
    del main_logger
    