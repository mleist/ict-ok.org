# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1111,E1101,E0611,W0613,W0231
#
"""implementation of an usermanagement 
"""

__version__ = "$Id$"

# python imports
from datetime import datetime
from pytz import timezone
import logging
from persistent.dict import PersistentDict

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import adapts, queryUtility
from zope.security.interfaces import IPrincipal
from zope.annotation.interfaces import IAnnotations
from zope.app.authentication.authentication import PluggableAuthentication
from zope.app.container.interfaces import IReadContainer
from zope.app.catalog.interfaces import ICatalog
from zope.traversing.api import getPath, getRoot, traverse
from zope.security.management import getInteraction
from zope.publisher.interfaces import IRequest
from zope.schema.fieldproperty import FieldProperty
from zope.app.container.contained import Contained

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

    #email = FieldProperty(IAdmUtilUserManagement['email'])

    def __init__(self):
        PluggableAuthentication.__init__(self)
        Supernode.__init__(self)
        self.ikRevision = __version__

    def getRequest(self):
        """ this trick will return the request from the working interaction
        see http://wiki.zope.org/zope3/FAQProgramming#how-do-i-get-irequest-object-in-event-handler
        """
        i = getInteraction() # raises NoInteraction
        for i_request in i.participations:
            if IRequest.providedBy(i_request):
                return i_request
        raise RuntimeError('Could not find current request.')

    # temp. workaround for "user specific email" in normal form
    def get_shortEmail(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(self.getRequest().principal).shortEmail
        except KeyError, errText:
            AdmUtilUserProperties(self.getRequest().principal).shortEmail = u""
    def set_shortEmail(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(self.getRequest().principal).shortEmail = my_val
    shortEmail = property(get_shortEmail, set_shortEmail)
    
    # temp. workaround for "user specific email" in normal form
    def get_email(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(self.getRequest().principal).email
        except KeyError, errText:
            AdmUtilUserProperties(self.getRequest().principal).email = u""
    def set_email(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(self.getRequest().principal).email = my_val
    email = property(get_email, set_email)
    
    # temp. workaround for "user specific timezone" in normal form
    def get_timezone(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(self.getRequest().principal).timezone
        except KeyError, errText:
            AdmUtilUserProperties(self.getRequest().principal).timezone = u""
    def set_timezone(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(self.getRequest().principal).timezone = my_val
    timezone = property(get_timezone, set_timezone)
    
    # temp. workaround for "user specific notifierLevel" in normal form
    def get_notifierLevel(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(\
                self.getRequest().principal).notifierLevel
        except KeyError, errText:
            AdmUtilUserProperties(\
                self.getRequest().principal).notifierLevel = u"warning"
    def set_notifierLevel(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(\
            self.getRequest().principal).notifierLevel = my_val
    notifierLevel = property(get_notifierLevel, set_notifierLevel)
    
    # temp. workaround for "user specific shortNotifierLevel" in normal form
    def get_shortNotifierLevel(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(\
                self.getRequest().principal).shortNotifierLevel
        except KeyError, errText:
            AdmUtilUserProperties(\
                self.getRequest().principal).shortNotifierLevel = u"error"
    def set_shortNotifierLevel(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(\
            self.getRequest().principal).shortNotifierLevel = my_val
    shortNotifierLevel = property(\
        get_shortNotifierLevel, set_shortNotifierLevel)
    


class AdmUtilUserDashboardSet(set):
    """ instance for storing dashboard items """
    def __contains__(self, obj):
        for item in self:
            if item == obj:
                return True
        return False
    def add(self, obj, arg_request=None):
        """ add a dashboard item to the dashboard set """
        if hasattr(obj, 'objectID'):
            my_catalog = zapi.getUtility(ICatalog)
            if len(my_catalog.searchResults(oid_index=obj.objectID)):
                return set.add(self, AdmUtilUserDashboardItem(obj, 'oid'))
            else: # object not in Catalog
                return set.add(self, AdmUtilUserDashboardItem(obj, 'path'))
        raise Exception, "wrong type for AdmUtilUserDashboardSet"
    def remove(self, obj, arg_request=None):
        """ remove a dashboard item from the dashboard set """
        for item in self:
            if item == AdmUtilUserDashboardItem(obj, item.stype):
                return set.remove(self, item)
        return False


class AdmUtilUserProperties(object):
    """major component for user properties"""

    implements(IAdmUtilUserProperties)
    adapts(IPrincipal)

    def __init__(self, context):
        annotations = IAnnotations(context)
        mapping = annotations.get(KEY)
        if mapping is None:
            blank = { 'shortEmail': u'',
                      'email': u'', 
                      'timezone': u'',
                      'notifierLevel': u"warning",
                      'shortNotifierLevel': u"error",
                      'dashboard_objs': AdmUtilUserDashboardSet()}
            mapping = annotations[KEY] = PersistentDict(blank)
        self.mapping = mapping
            
    shortEmail = MappingProperty('shortEmail')
    email = MappingProperty('email')
    timezone = MappingProperty('timezone')
    dashboard_objs = MappingProperty('dashboard_objs')
    notifierLevel = MappingProperty('notifierLevel')
    shortNotifierLevel = MappingProperty('shortNotifierLevel')


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
            elif hasattr(other, 'value'):
                return cmp(self.value, other.value)
            else:
                raise Exception, "other object '%s' doesn't have objectID" % \
                      other
        elif self.stype == 'path':
            if type(other) == type(u''):
                return cmp(self.value, other)
            elif type(other) == type(self):
                return cmp(self.value, other.value)
            else:
                return cmp(self.value, getPath(other))
        raise Exception, "wrong type for compare@AdmUtilUserDashboardItem"\
              " (%s[stype=%s], %s)" % (type(self), self.stype, \
                                       type(other))

    def getObject(self, some_obj=None, arg_request=None):
        """ get object from dashboard item """
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

def getUserTimezone():
    try:
        userManagement = queryUtility(IAdmUtilUserManagement)
        if userManagement is not None:
            return timezone(userManagement.timezone)
        else:
            return timezone("GMT")
    except:
        return timezone("GMT")

def convert2UserTimezone(timest):
    userTZ = getUserTimezone()
    if timest.tzinfo is None:
        return timest.replace(tzinfo=timezone("UTC")).astimezone(userTZ)
    else:
        return timest.astimezone(userTZ)
