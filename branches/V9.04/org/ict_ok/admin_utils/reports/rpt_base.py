# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py 350 2008-10-12 09:18:43Z markusleist $
#
# no_pylint: disable-msg=W0232
#
"""rpt_base classes for ict-ok.org reporting 
"""

__version__ = "$Id: $"


class RptSuperclass:
    """superclass for all reporting classes 
    """

    def __init__(self, arg_document = None):
        """
        constructor of the object
        """
        self._element_type = "superclass"
        self._document = arg_document
        self._content = []

    def __repr__(self):
        return u"IctReportSuperclass(%s)" % (self._content)

    def __str__(self):
        return u"superclass"

    def getDocument(self):
        return self._document

    def append(self, arg_obj):
        """
        append an object to the elements content
        """
        return self._content.append(arg_obj)

    def count(self, arg_obj):
        """
        return number of occurrences of an object in the elements content
        """
        return self._content.count(arg_obj)

    def index(self, arg_obj):
        """
        return first index of an object in the elements content
        """
        return self._content.index(arg_obj)

    def pop(self, index=None):
        """
        remove and return an object at index (default last)
        """
        return self._content.pop(index)

    def remove(self, index=None):
        """
        remove first occurrence of an object
        """
        return self._content.remove(index)
    
    def outConsole(self, indent=0):
        """
        output per print
        """
        print u"%s%s\n" % (" " * indent, self.__str__())
        #print u" " * indent + str(self.__str__())
        for myobj in self._content:
            if hasattr(myobj, "outConsole"):
                myobj.outConsole(indent+2)

    def outConsoleTree(self, indent=0):
        """
        output per print
        """
        #print u"%s(%s) %s\n" % ("-" * indent, self._element_type, self)
        #print u"%s%s\n" % ("-" * indent, self.__repr__())
        print u"%s%s:%s" % ("-" * indent, self._element_type, self.__str__())
        for myobj in self._content:
            try:
                myobj.outConsoleTree(indent+2)
            except:
                pass
                #print u"%s(%s) %s\n" % \
                      #("-" * indent, myobj._element_type, myobj)

if __name__ == '__main__':
    rpt_s1 = RptSuperclass()
    rpt_s1.outConsole()
