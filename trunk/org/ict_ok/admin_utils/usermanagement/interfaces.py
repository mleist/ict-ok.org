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
"""Interface of UserManagement-Utility"""

__version__ = "$Id$"

# python imports
import pytz

# zope imports
from zope.interface import Attribute, Interface, invariant, Invalid
from zope.schema import List, Object, TextLine, Choice, Password
from zope.i18nmessageid import MessageFactory
from zope.app.security.interfaces import IAuthentication

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.schema.emailvalid import EmailValid

_ = MessageFactory('org.ict_ok')


class IAdmUtilUserProperties(Interface):
    """
    major component for user properties
    """

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


class IAdmUtilUserManagement(ISupernode, IAuthentication):
    """
    major component for user registration and management
    """
    email = EmailValid(
        title = _(u"Email address"),
        required=False
        )
    timezone = Choice(
        title=_("Time Zone"),
        description=_("Time Zone used to display your calendar"),
        values=pytz.common_timezones,
        required = False)

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

