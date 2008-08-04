# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of Script

Script does ....

"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from RestrictedPython import compile_restricted

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.script.interfaces import IScript

class Script(Component):
    """
    the template instance
    """

    implements(IScript)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    pythonScript = FieldProperty(IScript['pythonScript'])
    printHistory = FieldProperty(IScript['printHistory'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        for (name, value) in data.items():
            if name in IScript.names():
                setattr(self, name, value)
        self.printHistory = []
        self.ikRevision = __version__

    def appendPrintHistory(self, printString):
        """
        will fill a list of 10 entries with the string-output
        from python functions
        """
        self.printHistory.append(printString)
        if len(self.printHistory) > 10:
            self.printHistory.pop(0)
        #print "appendPrintHistory: ", self.printHistory
        
    def tickerEvent(self):
        """
        got ticker event from ticker thread
        """
        print "Script.tickerEvent    ->"
        self.outputDebug()
        tmpScript = '''def hello_world():
                           return "Hello World!"
                           '''
        #tmpScript = "1+1"
        #print "ccc: ", 
        try:
            code = compile_restricted(tmpScript, '<string>', 'exec')
            exec(code)
            print "ddd: ", hello_world()
        except Exception, errText:
            self.appendPrintHistory(str(errText))
            self.appendHistoryEntry(str(errText))
        print "<--"
