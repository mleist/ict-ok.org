# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0102, W0613, W0702
#
"""implementation of Entry class for history
"""

__version__ = "$Id$"

# phython imports
from datetime import datetime

# zope imports
from persistent import Persistent

# ict_ok.org imports


class Entry(Persistent):
    """
    Entry class for history
    """
    entryVersion = 0x10
    
    def __init__(self, inData, inObject=None, level=u"warn"):
        # init with string
        if type(inData) == type("") or type(inData) == type(u""): 
            self._text = u"%s" % inData
            self._version = self.entryVersion
            self._objversion = None
            self._time = datetime.utcnow()
            self._level = u"%s" % level
            self._object = inObject
        # init with pickle
        elif type(inData) == type({}):
            if (inData.has_key('objClass')) and \
               (inData['objClass'] == 'Entry'):
                self._text = inData['text']
                self._version = inData['version']
                self._objversion = inData['objversion']
                self._time = inData['date']
                self._level = inData['level']
                self._object = inObject

    def setObjVersion(self, objversion=None):
        """ change Versioninfo for special Object"""
        if (objversion is not None) and \
           (objversion != self._objversion):
            self._objversion = objversion

    def getText(self):
        return self._text

    def getTime(self):
        return self._time

    def getLevel(self):
        return self._level

    def getList(self, fields=['date', 'text']):
        """
        return a list with history entries for html
        """
        retList = []
        for field in fields:
            if field == 'date':
                retList.append(self._time)
            elif field == 'text':
                retList.append(self._text)
            elif field == 'version':
                retList.append(self._version)
            elif field == 'level':
                try:
                    retList.append(self._level)
                except:
                    retList.append(u"-")
            elif field == 'bgcolor':
                try:
                    if self._level == "info":
                        retList.append(u"#E0E0FF")
                    elif self._level == "warn":
                        retList.append(u"#FFE0E0")
                    elif self._level == "err":
                        retList.append(u"#FF0000")
                    else:
                        retList.append(u"#FFFFFF")
                except:
                    retList.append(u"#FFFFFF")
            else:
                raise Exception, "Unknown field"
        return retList

    def exportAsDict(self, mode='backup'):
        """
        this will export special attributes of the object by python-pickle
        """
        retVal = {}
        retVal['objClass'] = self.__class__.__name__
        retVal['date'] = self._time
        retVal['text'] = self._text
        retVal['version'] = self._version
        retVal['objversion'] = self._objversion
        try:
            retVal['level'] = self._level
        except:
            retVal['level'] = u"-"
        return retVal
