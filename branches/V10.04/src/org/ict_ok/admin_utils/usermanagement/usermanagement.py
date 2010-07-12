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
#from ldap.filter import filter_format
import ldap

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import adapts, queryUtility, adapter
from zope.security.interfaces import IPrincipal
from zope.annotation.interfaces import IAnnotations
from zope.app import authentication
from zope.app.authentication.authentication import PluggableAuthentication
from zope.app.container.interfaces import IReadContainer
from zope.app.catalog.interfaces import ICatalog
from zope.traversing.api import getPath, getRoot, traverse
from zope.security.management import getInteraction
from zope.publisher.interfaces import IRequest
from zope.schema.fieldproperty import FieldProperty
from zope.app.container.contained import Contained
from zope.app.principalannotation.interfaces import IPrincipalAnnotationUtility
from ldapadapter.interfaces import IManageableLDAPAdapter, InvalidCredentials, \
    NoSuchObject, ServerDown

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.app.authentication.interfaces import IAuthenticatedPrincipalCreated, IAuthenticatorPlugin
from zope.app.component import queryNextUtility
# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.usermanagement.interfaces import \
     IAdmUtilUserDashboard, IAdmUtilUserDashboardItem,\
     IAdmUtilUserProperties, IAdmUtilUserManagement, \
     IAdmUtilUserPreferences, IEditPassword
#other imports
from ldappas.interfaces import ILDAPAuthentication
from ldappas.authentication import LDAPAuthentication
from ldapadapter.interfaces import ILDAPAdapter

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

    implements(IAdmUtilUserManagement, IAdmUtilUserPreferences, IEditPassword)
    adapts(IPrincipal)

    serverURL = FieldProperty(IAdmUtilUserManagement['serverURL'])
    baseDN = FieldProperty(IAdmUtilUserManagement['baseDN'])
    useLdap = FieldProperty(IAdmUtilUserManagement['useLdap'])
    bindDN = FieldProperty(IAdmUtilUserManagement['bindDN'])
    bindPassword = FieldProperty(IAdmUtilUserManagement['bindPassword'])
    useSSL =FieldProperty(IAdmUtilUserManagement['useSSL'])
    searchBase = FieldProperty(IAdmUtilUserManagement['searchBase'])
    searchScope = FieldProperty(IAdmUtilUserManagement['searchScope'])
    groupsSearchBase = FieldProperty(IAdmUtilUserManagement['groupsSearchBase'])
    groupsSearchScope = FieldProperty(IAdmUtilUserManagement['groupsSearchScope'])
    loginAttribute = FieldProperty(IAdmUtilUserManagement['loginAttribute'])
    idAttribute = FieldProperty(IAdmUtilUserManagement['idAttribute'])
    titleAttribute = FieldProperty(IAdmUtilUserManagement['titleAttribute'])
    groupIdAttribute = FieldProperty(IAdmUtilUserManagement['groupIdAttribute'])
    
    
    #email = FieldProperty(IAdmUtilUserManagement['email'])

    def __init__(self):
        PluggableAuthentication.__init__(self)
        Supernode.__init__(self)
        self.ikRevision = __version__

    def getAuthenticatorPlugins(self):
        authenticatorPlugins = list(self.authenticatorPlugins)
        if "LDAPAuthentication" in authenticatorPlugins:
            if not self.useLdap:
                authenticatorPlugins.remove("LDAPAuthentication")
        authenticatorPlugins = tuple(authenticatorPlugins)
        return self._plugins(authenticatorPlugins, IAuthenticatorPlugin)

    def getRequest(self):
        """ this trick will return the request from the working interaction
        see http://wiki.zope.org/zope3/FAQProgramming#how-do-i-get-irequest-object-in-event-handler
        """
        i = getInteraction() # raises NoInteraction
        for i_request in i.participations:
            if IRequest.providedBy(i_request):
                return i_request
        raise RuntimeError('Could not find current request.')

    # temp. workaround for "user specific timezone" in normal form
    def get_timezone(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(self.getRequest().principal).timezone
        except KeyError, errText:
            AdmUtilUserProperties(self.getRequest().principal).timezone = u""
            return AdmUtilUserProperties(self.getRequest().principal).timezone
    def set_timezone(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(self.getRequest().principal).timezone = my_val
    timezone = property(get_timezone, set_timezone)

    # temp. workaround for "user specific list Length" in normal form
    def get_listLen(self):
        """ property getter"""
        principal = self.getRequest().principal
        try:
            return AdmUtilUserProperties(principal).listLen
        except KeyError, errText:
            AdmUtilUserProperties(principal).listLen = 20
            return AdmUtilUserProperties(principal).listLen
    def set_listLen(self, my_val):
        """ property setter"""
        principal = self.getRequest().principal
        AdmUtilUserProperties(principal).listLen = my_val
    listLen = property(get_listLen, set_listLen)

    # temp. workaround for "user specific compactView" in normal form
    def get_compactView(self):
        """ property getter"""
        principal = self.getRequest().principal
        try:
            return AdmUtilUserProperties(principal).compactView
        except KeyError, errText:
            AdmUtilUserProperties(principal).compactView = False
            return AdmUtilUserProperties(principal).compactView
    def set_compactView(self, my_val):
        """ property setter"""
        principal = self.getRequest().principal
        AdmUtilUserProperties(principal).compactView = my_val
    compactView = property(get_compactView, set_compactView)

    # temp. workaround for "user specific navExplanation" in normal form
    def get_navExplanation(self):
        """ property getter"""
        principal = self.getRequest().principal
        try:
            return AdmUtilUserProperties(principal).navExplanation
        except KeyError, errText:
            AdmUtilUserProperties(principal).navExplanation = False
            return AdmUtilUserProperties(principal).navExplanation
    def set_navExplanation(self, my_val):
        """ property setter"""
        principal = self.getRequest().principal
        AdmUtilUserProperties(principal).navExplanation = my_val
    navExplanation = property(get_navExplanation, set_navExplanation)

    # temp. workaround for "user specific email" in normal form
    def get_email(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(self.getRequest().principal).email
        except KeyError, errText:
            AdmUtilUserProperties(self.getRequest().principal).email = u""
            return AdmUtilUserProperties(self.getRequest().principal).timezone
    def set_email(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(self.getRequest().principal).email = my_val
    email = property(get_email, set_email)
    
    # temp. workaround for "user specific email" in normal form
    def get_startView(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(self.getRequest().principal).startView
        except KeyError, errText:
            AdmUtilUserProperties(self.getRequest().principal).startView = "view_dashboard.html"
            return AdmUtilUserProperties(self.getRequest().principal).startView
    def set_startView(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(self.getRequest().principal).startView = my_val
    startView = property(get_startView, set_startView)
    
    # temp. workaround for "user specific notifierLevel" in normal form
    def get_notifierChannels(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(\
                self.getRequest().principal).notifierChannels
        except KeyError, errText:
            AdmUtilUserProperties(\
                self.getRequest().principal).notifierChannels = set([])
            return AdmUtilUserProperties(\
                self.getRequest().principal).notifierChannels
    def set_notifierChannels(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(\
            self.getRequest().principal).notifierChannels = my_val
    notifierChannels = property(get_notifierChannels,
                                set_notifierChannels)

    # temp. workaround for "user specific notifierLevel" in normal form
    def get_notifierLevel(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(\
                self.getRequest().principal).notifierLevel
        except KeyError, errText:
            AdmUtilUserProperties(\
                self.getRequest().principal).notifierLevel = 100
            return AdmUtilUserProperties(\
                self.getRequest().principal).notifierLevel
    def set_notifierLevel(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(\
            self.getRequest().principal).notifierLevel = my_val
    notifierLevel = property(get_notifierLevel, set_notifierLevel)
    
    # temp. workaround for "user specific email" in normal form
    def get_shortEmail(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(self.getRequest().principal).shortEmail
        except KeyError, errText:
            AdmUtilUserProperties(self.getRequest().principal).shortEmail = u""
            return AdmUtilUserProperties(self.getRequest().principal).shortEmail
    def set_shortEmail(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(self.getRequest().principal).shortEmail = my_val
    shortEmail = property(get_shortEmail, set_shortEmail)
    
    # temp. workaround for "user specific notifierLevel" in normal form
    def get_shortNotifierChannels(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(\
                self.getRequest().principal).shortNotifierChannels
        except KeyError, errText:
            AdmUtilUserProperties(\
                self.getRequest().principal).shortNotifierChannels = set([])
            return AdmUtilUserProperties(\
                self.getRequest().principal).shortNotifierChannels
    def set_shortNotifierChannels(self, my_val):
        """ property setter"""
        AdmUtilUserProperties(\
            self.getRequest().principal).shortNotifierChannels = my_val
    shortNotifierChannels = property(get_shortNotifierChannels,
                                     set_shortNotifierChannels)

    # temp. workaround for "user specific shortNotifierLevel" in normal form
    def get_shortNotifierLevel(self):
        """ property getter"""
        try:
            return AdmUtilUserProperties(\
                self.getRequest().principal).shortNotifierLevel
        except KeyError, errText:
            AdmUtilUserProperties(\
                self.getRequest().principal).shortNotifierLevel = 1000
            return AdmUtilUserProperties(\
                self.getRequest().principal).shortNotifierLevel
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
            blank = { 'timezone': u'',
                      'listLen': 20,
                      'navExplanation': False,
                      'compactView': False,
                      'email': u'',
                      'startView': u'view_dashboard.html',
                      'notifierChannels': set([]),
                      'notifierLevel': 100,
                      'shortEmail': u'',
                      'shortNotifierChannels': set([]),
                      'shortNotifierLevel': 1000,
                      'dashboard_objs': AdmUtilUserDashboardSet()}
            mapping = annotations[KEY] = PersistentDict(blank)
        self.mapping = mapping
            
    email = MappingProperty('email')
    listLen = MappingProperty('listLen')
    navExplanation = MappingProperty('navExplanation')
    compactView = MappingProperty('compactView')
    startView = MappingProperty('startView')
    notifierChannels = MappingProperty('notifierChannels')
    notifierLevel = MappingProperty('notifierLevel')
    shortEmail = MappingProperty('shortEmail')
    shortNotifierChannels = MappingProperty('shortNotifierChannels')
    shortNotifierLevel = MappingProperty('shortNotifierLevel')
    timezone = MappingProperty('timezone')
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
    if not hasattr(timest, 'tzinfo') or \
        timest.tzinfo is None:
        return timest.replace(tzinfo=timezone("UTC")).astimezone(userTZ)
    else:
        return timest.astimezone(userTZ)

def getNotifierDict4User(principal_id):
    """will return notifier props for a special principal id
    """
    retDict = {'timezone': None,
               'startView': None,
               'email': None,
               'notifierChannels': None,
               'notifierLevel': None,
               'shortEmail': None,
               'shortNotifierChannels': None,
               'shortNotifierLevel': None,
               'shortEmail': None,
               }
    pr_anno_util = queryUtility(IPrincipalAnnotationUtility)
    principal_annos = pr_anno_util.getAnnotationsById(principal_id)
    if principal_annos:
        if principal_annos.data.has_key(KEY):
            for dictKey in retDict.keys():
                if principal_annos.data[KEY].has_key(dictKey):
                    retDict[dictKey] = principal_annos.data[KEY][dictKey]
    return retDict

def allLdapUser(dummy_context):
    """Ask the ldap for our user ĺist
    """
    terms = []
    userManagement = queryUtility(IAdmUtilUserManagement)
    if userManagement is not None and userManagement.useLdap:
        ldapUtil = queryUtility(IManageableLDAPAdapter,
                                name='ManageableLDAPAdapter')
        if ldapUtil.serverURL != userManagement.serverURL:
            ldapUtil.serverURL = userManagement.serverURL
        if ldapUtil.bindDN != userManagement.bindDN:
            ldapUtil.bindDN = userManagement.bindDN
        if ldapUtil.bindPassword != userManagement.bindPassword:
            ldapUtil.bindPassword = userManagement.bindPassword
        conn = ldapUtil.connect()
        ldapResultList = conn.search(userManagement.baseDN,
                          scope='sub',
                          filter='(objectClass=*)',
                          attrs=['uid', 'cn'])
        ldapResultList.sort()
        for ldapKey, ldapDict in ldapResultList:
            if ldapDict.has_key('cn'):
                terms.append(\
                    SimpleTerm(ldapKey,
                               token=str(ldapKey),
                               title=ldapDict['cn'][0]))
        conn.conn.unbind()
    return SimpleVocabulary(terms)

def UserCfgStartView(dummy_context):
    terms = []
    for (gkey, gname) in {
        "overview.html": u"Overview",
        "view_dashboard.html": u"Dashboard",
        "focus.html": u"Focus",
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

class MyLDAPAuthentication(LDAPAuthentication):

    implements(
        ILDAPAuthentication,
        authentication.groupfolder.IGroupFolder,
        authentication.interfaces.IAuthenticatorPlugin,
        authentication.interfaces.IQueriableAuthenticator,
        authentication.interfaces.IQuerySchemaSearch)
    
    def __init__(self, prefix=u'ldap.'):
        super(MyLDAPAuthentication, self).__init__()
        self.prefix = prefix

    def __contains__(self, key):
        # ToDo: What's up
        #print "__contains__(%s, %s)" % (self, key)
        #return len(self.getGroupsForPrincipal(self.prefix+key))>0
        return False

    def __len__(self):
        return 0

    def __iter__(self):
        return iter([])

    def getLDAPAdapter(self):
        """Get the LDAP adapter according to our configuration.
        and sets all needed attributes
        """
        ldapAdapter = queryUtility(ILDAPAdapter, self.adapterName)
        self.setLDAPAdapterAttrs(ldapAdapter)
        return ldapAdapter

    def setLDAPAdapterAttrs(self, ldapAdapter):
        """ Sets LDAP Attributes from our AdmUtilUserManagement
        """
        userManagement = queryUtility(IAdmUtilUserManagement)
        if userManagement is None:
            raise Exception
        if ldapAdapter.serverURL != userManagement.serverURL:
            ldapAdapter._setServerURL(userManagement.serverURL)
        if ldapAdapter.bindDN != userManagement.bindDN:
            ldapAdapter.bindDN = userManagement.bindDN
        if ldapAdapter.bindPassword != userManagement.bindPassword and userManagement.bindPassword is not None:
            ldapAdapter.bindPassword = userManagement.bindPassword
        if ldapAdapter.useSSL != userManagement.useSSL:
            ldapAdapter.useSSL = userManagement.useSSL
            
        if self.searchBase != userManagement.searchBase:
            self.searchBase = userManagement.searchBase
        if self.searchScope != userManagement.searchScope:
            self.searchScope = userManagement.searchScope
        if self.groupsSearchBase != userManagement.groupsSearchBase:
            self.groupsSearchBase = userManagement.groupsSearchBase
        if self.groupsSearchScope != userManagement.groupsSearchScope:
            self.groupsSearchScope = userManagement.groupsSearchScope
        if self.loginAttribute != userManagement.loginAttribute:
            self.loginAttribute = userManagement.loginAttribute
        if self.idAttribute != userManagement.idAttribute:
            self.idAttribute = userManagement.idAttribute
        if self.titleAttribute != userManagement.titleAttribute:
            self.titleAttribute = userManagement.titleAttribute
        if self.groupIdAttribute != userManagement.groupIdAttribute:
            self.groupIdAttribute = userManagement.groupIdAttribute

    def getGroupsForPrincipal(self, principalid):
        """Get groups the given principal belongs to"""
        searchObjectclass = u'groupOfNames'
        #searchMember = u'uid=%s,ou=personal,o=ikom-online,c=de,dc=ifdd' % principalid[len(self.prefix):]
        searchMember = u'%s=%s,%s' % (self.loginAttribute, principalid[len(self.prefix):], self.searchBase)
        return self.groupsSearch({'objectClass':searchObjectclass,
                                  'member':searchMember})

    def getPrincipalsForGroup(self, groupid):
        """Get principals which belong to the group"""
        return []
    
    def groupsSearch(self, query):
        """See zope.app.authentication.interfaces.IQuerySchemaSearch."""
        da = self.getLDAPAdapter()
        if da is None:
            return ()
        try:
            conn = da.connect()
        except InvalidCredentials:
            return ()
        except ServerDown:
            return ()
        except ldap.INVALID_DN_SYNTAX:
            return ()

        # Build the filter based on the query
        filter_elems = []
        for key, value in query.items():
            if not value:
                continue
            filter_elems.append(ldap.filter.filter_format('(%s=%s)',
                                                          (key, value)))
        filter = ''.join(filter_elems)
        if len(filter_elems) > 1:
            filter = '(&%s)' % filter

        if not filter:
            filter = '(objectClass=*)'

        try:
            res = conn.search(self.groupsSearchBase, self.groupsSearchScope, filter=filter,
                              attrs=[self.groupIdAttribute])
        except NoSuchObject, errText:
            print "NoSuchObject: errText: ", errText
            return ()
        except KeyError, errText:
            print "KeyError: errText: ", errText
            return ()

        prefix = self.principalIdPrefix
        #prefix = u'group.'
        infos = []
        for dn, entry in res:
            try:
                infos.append(prefix+entry[self.groupIdAttribute][0])
            except (KeyError, IndexError):
                pass
        return infos
