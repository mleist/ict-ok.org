# -*- coding: utf-8 -*-
#
# $Id$
#
# pylint: disable-msg=W0201
#
"""
Helper-Classes for the agents of ict-ok.org
"""

__version__ = "$Id$"
__versRevision = "$LastChangedRevision$"

# phython imports
import logging, logging.handlers

class IkLogger:
    def __init__( self, appName):
        """
        initialize the ikomtrol logger
        """
        self.log = logging.getLogger( appName)
        self.log.setLevel( logging.DEBUG)
        logging.basicConfig( level = logging.DEBUG,
                             format = '%(asctime)s [%(name)s] %(levelname)s --> %(message)s',
                             filename = '/tmp/ikDebug.txt',
                             filemode = 'a'
                         )
        self.log.info( "Logger startet")

if __name__ == "__main__":
    testLogger = IkLogger( "ik_logger.py")
    del testLogger
    print "don't do this"
