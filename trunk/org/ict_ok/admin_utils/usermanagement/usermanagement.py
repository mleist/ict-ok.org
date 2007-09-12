# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1111,E0611,W0613,W0231
#
"""implementation of an usermanagement 
"""

__version__ = "$Id$"

# phython imports
import logging
from persistent.dict import PersistentDict
from persistent import Persistent
from zope.app.container.contained import Contained

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import adapts
from zope.security.interfaces import IPrincipal
from zope.annotation.interfaces import IAnnotations
from zope.app.authentication.authentication import PluggableAuthentication
from zope.app.container.interfaces import IReadContainer
from zope.app.catalog.interfaces import ICatalog
from zope.traversing.api import getPath, getRoot, traverse

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.usermanagement.interfaces import \
     IAdmUtilUserDashboard, IAdmUtilUserDashboardItem,\
     IAdmUtilUserProperties, IAdmUtilUserManagement

logger = logging.getLogger("AdmUtilUserManagement")

KEY = "org.ict_ok.admin_utils.usermanagement"

class MappingProperty(object):
    """
    helper class for properties
    """
    def __init__(self, name):
        self.name = name
    
    def __get__(self, inst, class_=None):
        return inst.mapping[self.name]
    
    def __set__(self, inst, value):
        inst.mapping[self.name] = value



class AdmUtilUserManagement(Supernode, PluggableAuthentication):
    """Implementation of local UserManagement Utility"""

    implements(IAdmUtilUserManagement)
    adapts(IPrincipal)

    def __init__(self):
        PluggableAuthentication.__init__(self)
        Supernode.__init__(self)
        self.ikRevision = __version__

class AdmUtilUserDashboardSet(set):
    def __contains__(self, obj):
        print "__contains__(%s, %s)" % (self, obj)
        for item in self:
            if item == obj:
                return True
        return False
    def add(self, obj, arg_request=None):
        if hasattr(obj, 'objectID'):
            my_catalog = zapi.getUtility(ICatalog)
            if len(my_catalog.searchResults(oid_index=obj.objectID)):
                set.add(self, AdmUtilUserDashboardItem(obj, 'oid'))
                return True
            else: # object not in Catalog
                set.add(self, AdmUtilUserDashboardItem(obj, 'path'))
                from zope.traversing.api import getPath
                aa=getPath(obj)
                from zope.traversing.api import getRoot,traverse
                if arg_request is not None:
                    bb=traverse(getRoot(obj), aa, request=arg_request)
                return True
        raise Exception, "wrong type for AdmUtilUserDashboardSet"
    def remove(self, obj, arg_request=None):
        import pdb;pdb.set_trace()
        for item in self:
            if item == obj:
                return set.remove(item)
        return False


#class AdmUtilUserProperties(Persistent, Contained):
class AdmUtilUserProperties(object):
    """major component for user properties"""

    implements(IAdmUtilUserProperties)
    adapts(IPrincipal)

    def __init__(self, context):
        annotations = IAnnotations(context)
        mapping = annotations.get(KEY)
        if mapping is None:
            blank = { 'email': u'', 
                      'dashboard_objs': AdmUtilUserDashboardSet()}
            mapping = annotations[KEY] = PersistentDict(blank)
        self.mapping = mapping
            
    email = MappingProperty('email')
    dashboard_objs = MappingProperty('dashboard_objs')

class AdmUtilUserDashboard(Contained):
    """ user dashboard """
    implements(IAdmUtilUserDashboard, IReadContainer)
    
    def __init__(self):
        Contained.__init__(self)

    def __getitem__(self, key):
        '''See interface `IReadContainer`'''
        print "AdmUtilUserDashboard.__getitem__(%s)" % (key)
        
    def values(self):
        '''See interface `IReadContainer`'''
        print "AdmUtilUserDashboard.values"

class AdmUtilUserDashboardItem(object):
    """ item of user dashboard """
    implements(IAdmUtilUserDashboardItem)

    def __init__(self, obj, stype='oid'):
        self.stype = stype
        if self.stype == 'oid':
            self.value = obj.getObjectId()
        elif self.stype == 'path':
            self.value = getPath(obj)
    def __cmp__(self, other):
        if self.stype == 'oid':
            if hasattr(other, 'objectID'):
                return cmp(self.value, other.objectID)
        elif self.stype == 'path':
            return cmp(self.value,getPath(other))
        raise Exception, "wrong type for compare@AdmUtilUserDashboardItem"
    def getObject(self, some_obj=None, arg_request=None):
        if self.stype == 'oid':
            my_catalog = zapi.getUtility(ICatalog)
            resultList = my_catalog.searchResults(oid_index=self.value)
            if len(resultList) > 0:
                return iter(resultList).next()
            else:
                return None
        elif self.stype == 'path':
            if some_obj is not None and arg_request is not None:
                return traverse(getRoot(some_obj),
                                self.value,
                                request=arg_request)
        raise Exception, "wrong type for getObject@AdmUtilUserDashboardItem"
        
        
