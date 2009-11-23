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

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from RestrictedPython import compile_restricted

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.script.interfaces import IScript


class ScriptPrinter:
    '''Will drop the print output to the object history
    '''
    def __init__(self, scriptObj=None):
        self.scriptObj = scriptObj
        self.txt = []
    def write(self, text):
        self.txt.append(text)
    def __call__(self):
        self.scriptObj.appendHistoryEntry(''.join(self.txt))

class Script(Component):
    """
    the template instance
    """

    implements(IScript)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    pythonScript = FieldProperty(IScript['pythonScript'])

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
        if True:
            return
        print "Script.tickerEvent    ->"
        self.outputDebug()
        #tmpScript = '''print "abba1"
#print "abba2"
#print "abba3"
#print "abba4"
#def hello_world():
    #return "Hello World!"
#result = printed
#'''
        #tmpScript = "1+1"
        #print "ccc: ", 
        try:
            from RestrictedPython.PrintCollector import PrintCollector
            from RestrictedPython.Guards import safe_builtins
            from RestrictedPython.Guards import full_write_guard
            restricted_globals = dict(__builtins__ = safe_builtins)
            tmpScript = self.pythonScript + "\n" + "result = printed"
            restricted_globals['_print_'] = PrintCollector
            restricted_globals['dir'] = __builtins__['dir']
            restricted_globals['type'] = __builtins__['type']
            restricted_globals['globals'] = __builtins__['globals']
            restricted_globals['locals'] = __builtins__['locals']
            restricted_globals['context'] = self
            restricted_globals['_write_'] = full_write_guard
            restricted_globals['_getattr_'] = getattr
            code = compile_restricted(tmpScript, '<string>', 'exec')
            exec(code) in restricted_globals
            #print "ddd: ", hello_world()
            #print "eee: ", restricted_globals['result']
            self.appendHistoryEntry(restricted_globals['result'])
        except Exception, errText:
            print "err1:", str(errText)
            print "err2:", dir(errText)
            #self.appendPrintHistory(str(errText))
            self.appendHistoryEntry(str(errText), level="err")
        print "<--"
