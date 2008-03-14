# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""implementation of a "esx_vim daemon" 
"""

__version__ = "$Id$"

# phython imports
from datetime import datetime, timedelta

# zope imports
from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from zope.app.container.interfaces import IReadContainer

# ict_ok.org imports
from org.ict_ok.admin_utils.esx_vim.esx_vim_obj import EsxVimObj
from org.ict_ok.admin_utils.esx_vim.interfaces import \
     IEsxVimFolder
from org.ict_ok.admin_utils.esx_vim.esx_vim import globalEsxVimUtility


_ = MessageFactory('org.ict_ok')

dictEsxVimFolderGetItems = {}
dictEsxVimFolderGetItemCacheTime = {}
dictEsxVimFolderValues = {}
dictEsxVimFolderValuesCacheTime = {}

class EsxVimFolder(EsxVimObj):
    """
    These are generic folders for storing inventory objects.
    """
    implements(IEsxVimFolder, IReadContainer)
    def __init__(self):
        EsxVimObj.__init__(self)
        self.esxObjectTypes = None
        dictEsxVimFolderGetItemCacheTime[self.objectID] = datetime.utcnow() \
                                        - timedelta(seconds=60)
        dictEsxVimFolderValuesCacheTime[self.objectID] = \
                                       dictEsxVimFolderGetItemCacheTime[self.objectID]
        dictEsxVimFolderGetItems[self.objectID] = None
        dictEsxVimFolderValues[self.objectID] = None

    def __getitem__(self, key):
        '''See interface `IReadContainer`'''
        print "EsxVimFolder.__getitem__(%s)" % (key)
        nowTime = datetime.utcnow()
        deltaTime = nowTime - dictEsxVimFolderGetItemCacheTime[self.objectID]
        if deltaTime > timedelta(seconds=30):
            print "in cache"
            dictEsxVimFolderGetItemCacheTime[self.objectID] = nowTime
            myParams = {\
                'cmd': 'find_entity_views',
                'view_type': self.esxObjectTypes,
                'admUtilEsxVim': self.localEsxUtil,
                }
            myDict = globalEsxVimUtility.get_EsxVimObject_Dict(myParams, self)
            #myDict = globalEsxVimUtility.get_EsxVimAllDict(self, self)
            print "myDict:", myDict
            myObj = myDict[key]
            print "myObj:", myObj
            dictEsxVimFolderGetItems[self.objectID] = myObj
            #return myObj
        else:
            print "Cached"
        return dictEsxVimFolderGetItems[self.objectID]
        #return globalEsxVimUtility.get_EsxVimDatacenter_Dict(self, self)[key]
        #return globalEsxVimUtility.get_EsxVimDatacenter_Dict(self, self)[key]
        
    def get(self, key, default=None):
        '''See interface `IReadContainer`'''
        #if self.__data.has_key(key):
            #return self.__data.get(key, default)
        #else:
        return self.__getitem__(key)


    def values(self):
        '''See interface `IReadContainer`'''
        print "EsxVimFolder.values"
        #return globalEsxVimUtility.get_EsxVimDatacenter_values(self)
        nowTime = datetime.utcnow()
        deltaTime = nowTime - dictEsxVimFolderValuesCacheTime[self.objectID]
        if deltaTime > timedelta(seconds=30):
            print "in cache"
            dictEsxVimFolderValuesCacheTime[self.objectID] = nowTime
            myParams = {\
                'cmd': 'find_entity_views',
                'view_type': self.esxObjectTypes,
                'admUtilEsxVim': self.localEsxUtil,
                }
            dictEsxVimFolderValues[self.objectID] = \
                                  globalEsxVimUtility.get_EsxVimObject_Dict(myParams,
                                                                            self).values()
        else:
            print "Cached"
        return dictEsxVimFolderValues[self.objectID]
