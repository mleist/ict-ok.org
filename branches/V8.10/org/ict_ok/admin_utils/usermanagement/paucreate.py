# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1111,E0611,W0613
#
"""implementation of an automatic generation of PAU 
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app.security.interfaces import IAuthentication
from zope.app.authentication.interfaces import IAuthenticatorPlugin
from zope.app.appsetup.bootstrap import ensureUtility
from zope.app.authentication.authentication import \
     PluggableAuthentication
from zope.app.authentication.principalfolder import \
     InternalPrincipal, PrincipalFolder
from zope.app.authentication.groupfolder import \
     GroupFolder, GroupInformation

# ict_ok.org imports

#logger = logging.getLogger("AdmUtilUserManagement")
groups = [{'id': 'management',
           'title': 'Management',
           'description': 'Management der Firma XY'},
       ]

def addUtilityToPAU(pau, interface, utility_factory, arg_id, name, root_obj):
    """
    adds new Utility for existing PAU
    """
    utility = utility_factory()
    pau[arg_id] = utility
    sitem = root_obj.getSiteManager()
    sitem[name] = utility
    sitem.registerUtility(utility, interface)


def _addGroupInformation(group_folder, arg_id, title, description):
    """
    adds new group to a group folder
    """
    group = GroupInformation()
    group.title = title
    group.description = description
    group_folder[arg_id] = group

def _addPrincipal(principal_folder, arg_id, title, description):
    """
    adds new group to a group folder
    """
    principal = InternalPrincipal(arg_id, arg_id, title, description)
    principal_folder[arg_id] = principal

def createAuthenticationUtils(obj):
    """
    creates PAU and all the containing objects
    """
    madePluggableAuthentication = ensureUtility(\
        obj,
        IAuthentication,
        '',
        PluggableAuthentication,
        copy_to_zlog=False,
        asObject=True)

    if madePluggableAuthentication:
        auth = madePluggableAuthentication
        auth.credentialsPlugins = (u'Session Credentials',)
        addUtilityToPAU(auth, IAuthenticatorPlugin, PrincipalFolder,
                        'principal_folder', u'Benutzerverwaltung', obj)
        addUtilityToPAU(auth, IAuthenticatorPlugin, GroupFolder,
                        'group_folder', u'Gruppenverwaltung', obj)
        auth.authenticatorPlugins = (u'Benutzerverwaltung',
                                     u'Gruppenverwaltung',)
        group_folder = auth['group_folder']
        for group in groups:
            _addGroupInformation(group_folder, group['id'],
                                 group['title'], group['description'])
        principal_folder = auth['principal_folder']
        _addPrincipal(principal_folder, "markus", "markus", "Markus Leist")
