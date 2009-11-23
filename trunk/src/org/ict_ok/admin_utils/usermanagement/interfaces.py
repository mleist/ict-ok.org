# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
from zope.schema._bootstrapfields import TextLine
"""Interface of UserManagement-Utility"""

__version__ = "$Id$"

# python imports
import pytz

# zope imports
from zope.interface import Attribute, Interface, invariant, Invalid
from zope.schema import Choice, Password, Set, URI, Bool
from zope.i18nmessageid import MessageFactory
from zope.app.security.interfaces import IAuthentication

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.schema.emailvalid import EmailValid

#other imports
from ldappas.interfaces import ILDAPAuthentication

_ = MessageFactory('org.ict_ok')


class IAdmUtilUserProperties(Interface):
    """
    major component for user properties
    """
    shortEmail = EmailValid(
        title = _(u"Short email address"),
        required=False
        )

    email = EmailValid(
        title = _(u"Email address"),
        required=False
        )

    timezone = Choice(
        title=_("Time Zone"),
        values=pytz.common_timezones,
        required = False)

    #dashboard_obj_ids = List(
        #title = _("listoh objects for the dashboard"),
        #value_type = Object(
            #title = _("Object"))
    #)
    dashboard_objs = Attribute("list of object ids for the dashboard")


#class IAdmUtilUserManagement(Interface):
class IAdmUtilUserManagement(IAuthentication):
    """
    major component for user registration and management
    """
    useLdap = Bool(
        title = _("Usersearch by LDAP"),
        description = _("uses same LDAP connects"),
        default = False,
        required = False)
    serverURL = URI(
        max_length = 200,
        title = _("LDAP Server URL"),
        default = "ldap://127.0.0.1:389",
        required = False)
    baseDN = TextLine(
        max_length = 200,
        title = _("LDAP search base"),
        default = u"ou=staff,o=ict-ok,c=org",
        required = False)
    bindDN = TextLine(
        max_length = 200,
        title = _("LDAP bindDN"),
        default = u"ou=staff,o=ict-ok,c=org",
        required = False)
    bindPassword = TextLine(
        max_length = 200,
        title = _("Bind Password"),
        default = u"",
        required = False)
    useSSL = Bool(
        title = _("Use SSL on LDAP connect"),
        description = _("Use SSL on LDAP connect"),
        default = False,
        required = False)

    searchBase = TextLine(
        max_length = 200,
        title = _("Search Base"),
        default = u'ou=staff,o=ikom-online,c=de,o=ifdd',
        required = False)
    searchScope = Choice(
        title = _("Search Scope"),
        default = u'sub',
        values = [u'sub', u'one', u'base'],
        required = False)
    groupsSearchBase = TextLine(
        max_length = 200,
        title = _("Groups Search Base"),
        default = u'cn=testIKOMtrol,o=ikom-online,c=de,o=ifdd',
        required = False)
    groupsSearchScope = TextLine(
        max_length = 200,
        title = _("Groups Search Scope"),
        default = u'one',
        required = False)
    loginAttribute = TextLine(
        max_length = 200,
        title = _("Login Attribute"),
        default = u'uid',
        required = False)
    idAttribute = TextLine(
        max_length = 200,
        title = _("Id Attribute"),
        default = u'uid',
        required = False)
    titleAttribute = TextLine(
        max_length = 200,
        title = _("Title Attribute"),
        default = u'cn',
        required = False)
    groupIdAttribute = TextLine(
        max_length = 200,
        title = _("Group Id Attribute"),
        default = u'cn',
        required = False)


class IAdmUtilUserPreferences(Interface):
    """
    major component for user registration and management
    """
    timezone = Choice(
        title=_("Time Zone"),
        description=_("Time Zone used to display your calendar"),
        values=pytz.common_timezones,
        required = False)
    email = EmailValid(
        title = _(u"Email address"),
        required=False
        )
    startView = Choice(
        title=_("Start View"),
        default=u"view_dashboard.html",
        required = True,
        vocabulary = "UserCfgStartView")
    
    notifierChannels = Set(
        title = _("Notifier channels"),
        value_type = Choice(
            title = _("notifier channel"),
            vocabulary="notifierChannels"),
        default = set([]),
        readonly = False,
        required = True)
    notifierLevel = Choice(
        title=_("Notifier level"),
        description=_("minimum notification level"),
        default=u"warning",
        required = True,
        vocabulary = "notifierLevels")

    shortEmail = EmailValid(
        title = _(u"Short email address"),
        required=False
        )
    shortNotifierChannels = Set(
        title = _("Short notifier channels"),
        value_type = Choice(
            title = _("notifier channel"),
            vocabulary="notifierChannels"),
        default = set([]),
        readonly = False,
        required = True)
    shortNotifierLevel = Choice(
        title=_("Short notifier level"),
        description=_("minimum notification level for short messages"),
        default=u"error",
        required = True,
        vocabulary = "notifierLevels")


class IEditPassword(Interface):
    """ schema for user password dialog """
    password_old = Password(
        title = _(u"Old password"),
        required=True
        )
    password1 = Password(
        title = _(u"Password"),
        min_length = 4,
        max_length = 20,
        required=True
        )
    password2 = Password(
        title = _(u"Password (again)"),
        min_length = 4,
        max_length = 20,
        required=True
        )
    @invariant
    def ensureP1eqP2(data_set):
        """Password 1 and password 2 must be equal
        """
        if hasattr(data_set, "password1") and \
           hasattr(data_set, "password2") and \
           data_set.password1 != data_set.password2:
            raise Invalid("new passwords not equal")
    
class IAdmUtilUserDashboard(Interface):
    """ user dashboard """

class IAdmUtilUserDashboardItem(Interface):
    """ user dashboard """
    
class IMyLDAPAuthentication(ILDAPAuthentication):
    """ LDAP-specifc Autentication Plugin for the Pluggable Authentication.
    """
    

