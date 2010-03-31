# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611,W0612
#
"""startup of subsystem"""

__version__ = "$Id$"

# python imports
import logging
import transaction
from datetime import datetime

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.appsetup.bootstrap import ensureUtility
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.app.authentication.authentication import PluggableAuthentication
from zope.app.authentication.principalfolder import InternalPrincipal
from zope.app.authentication.principalfolder import PrincipalFolder
from zope.app.authentication.groupfolder import GroupInformation, \
     GroupFolder
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from ldapadapter.interfaces import IManageableLDAPAdapter
from ldapadapter.utility import ManageableLDAPAdapter
#from ldappas.interfaces import ILDAPAuthentication
#from ldappas.authentication import LDAPAuthentication

# ict_ok.org imports
from org.ict_ok.admin_utils.usermanagement.interfaces import \
     IAdmUtilUserManagement, IMyLDAPAuthentication
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     AdmUtilUserManagement, MyLDAPAuthentication

logger = logging.getLogger("AdmUtilUserManagement")

def createUtils(root_folder, connection=None, dummy_db=None):
    madeLdapAdapter = ensureUtility(\
        root_folder,
        IManageableLDAPAdapter,
        'ManageableLDAPAdapter',
        ManageableLDAPAdapter,
        name='ManageableLDAPAdapter',
        copy_to_zlog=False)

    madeLdapPas = ensureUtility(\
        root_folder,
        IMyLDAPAuthentication,
        'MyLDAPAuthentication',
        MyLDAPAuthentication,
        name='MyLDAPAuthentication',
        copy_to_zlog=False)

    if isinstance(madeLdapPas, MyLDAPAuthentication):
        madeLdapPas.adapterName = 'ManageableLDAPAdapter'
        #madeLdapPas.searchBase = u""
        #madeLdapPas.searchScope = u""
        #madeLdapPas.groupsSearchBase = u""
        #madeLdapPas.groupsSearchScope = u""
        #madeLdapPas.loginAttribute = u""
        madeLdapPas.principalIdPrefix = u'ldap.'
        #madeLdapPas.idAttribute = u""
        #madeLdapPas.titleAttribute = u""
        #madeLdapPas.groupIdAttribute = u""

    madePluggableAuthentication = ensureUtility(\
        root_folder,
        IAdmUtilUserManagement,
        'AdmUtilUserManagement',
        AdmUtilUserManagement,
        name='',
        copy_to_zlog=False)

    if isinstance(madePluggableAuthentication, PluggableAuthentication):
        logger.info(u"bootstrap: Ensure named AdmUtilUserManagement")
        dcore = IWriteZopeDublinCore(madePluggableAuthentication)
        dcore.title = u"User Authentication"
        dcore.created = datetime.utcnow()
        madePluggableAuthentication.ikName = dcore.title
        # madePluggableAuthentication.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made AdmUtilUserManagement-Utility")
        groups = GroupFolder(u'group.')
        madePluggableAuthentication[u'groups'] = groups
        principals = PrincipalFolder(u'principal.')
        madePluggableAuthentication[u'principals'] = principals
        madePluggableAuthentication.credentialsPlugins = \
                                   (u'Session Credentials',
                                    u'No Challenge if Authenticated',)
        p_user = InternalPrincipal(u'User', u'User',
                                   u'Initial User',
                                   passwordManagerName="SHA1")
        p_manager = InternalPrincipal(u'Manager', u'Manager',
                                      u'Initial Manager',
                                      passwordManagerName="SHA1")
        p_admin = InternalPrincipal(u'Administrator', u'Administrator',
                                    u'Initial Administrator',
                                    passwordManagerName="SHA1")
        p_developer = InternalPrincipal(u'Developer', u'Developer',
                                        u'Initial Developer',
                                        passwordManagerName="SHA1")
        principals[u'User'] = p_user
        principals[u'Manager'] = p_manager
        principals[u'Administrator'] = p_admin
        principals[u'Developer'] = p_developer
        grp_usr = GroupInformation(u'User',
                                   u'view & analyse data, generate reports '
                                   u'& leave notes at any object')
        grp_mgr = GroupInformation(u'Manager',
                                   u'search, connect, configure '
                                   u'& delete devices')
        grp_adm = GroupInformation(u'Administrator',
                                   u'install, configure '
                                   u'& administrate System')
        grp_dvl = GroupInformation(u'Developer',
                                   u'individual adaption '
                                   u'& development on System')
        grp_usr.principals = [u'principal.User']
        grp_mgr.principals = [u'principal.Manager']
        grp_adm.principals = [u'principal.Administrator']
        grp_dvl.principals = [u'principal.Developer']
        groups[u'User'] = grp_usr
        groups[u'Manager'] = grp_mgr
        groups[u'Administrator'] = grp_adm
        groups[u'Developer'] = grp_dvl
        madePluggableAuthentication[u'LDAPAuthentication'] = madeLdapPas
        madePluggableAuthentication.authenticatorPlugins = \
            (u'groups', u'principals', u'LDAPAuthentication')
        prm = IPrincipalRoleManager(root_folder)
        prm.assignRoleToPrincipal(u'org.ict_ok.usr', u'group.User')
        prm.assignRoleToPrincipal(u'org.ict_ok.mgr', u'group.Manager')
        prm.assignRoleToPrincipal(u'org.ict_ok.adm', u'group.Administrator')
        prm.assignRoleToPrincipal(u'org.ict_ok.dvl', u'group.Developer')



    transaction.get().commit()
    if connection is not None:
        connection.close()

def bootStrapSubscriberDatabase(event):
    """initialisation of usermanagement utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    createUtils(root_folder, connection, dummy_db)

