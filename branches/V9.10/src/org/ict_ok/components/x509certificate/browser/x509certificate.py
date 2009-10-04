# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of X509Certificate"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.security.proxy import removeSecurityProxy

# z3c imports
from z3c.form.browser import checkbox
from z3c.form.browser import file

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.superclass.browser.superclass import \
    Overview as SuperOverview
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm
from org.ict_ok.components.superclass.browser.superclass import \
    GetterColumn, DateGetterColumn, getStateIcon, raw_cell_formatter, \
    getHealth, getTitle, getModifiedDate, link, getActionBottons, IctGetterColumn
from org.ict_ok.components.credential.browser.credential import \
    CredentialDetails, CredentialFolderDetails
from org.ict_ok.components.x509certificate.interfaces import \
    IX509Certificate, IAddX509Certificate, IX509CertificateFolder
from org.ict_ok.components.x509certificate.x509certificate import X509Certificate
from org.ict_ok.components.browser.component import ComponentDetails

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddX509Certificate(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add X.509 Certificate')
    viewURL = 'add_x509certificate.html'
    weight = 50


class MGlobalAddX509Certificate(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add X.509 Certificate')
    viewURL = 'add_x509certificate.html'
    weight = 50
    folderInterface = IX509CertificateFolder

# --------------- object details ---------------------------


class X509CertificateDetails(CredentialDetails):
    """ Class for X509Certificate details
    """
    omit_viewfields = CredentialDetails.omit_viewfields + []
    omit_addfields = CredentialDetails.omit_addfields + []
    omit_editfields = CredentialDetails.omit_editfields + []
    
    def getIssuerName(self):
        issuer = removeSecurityProxy(self.context.getIssuerName())
        issue_str = u', '.join([u"%s=%s" % (i_k, i_v)
                                for i_k, i_v in issuer.get_components()])
        return issue_str

    def getSubject(self):
#        from ldappas.interfaces import ILDAPAuthentication
#        from zope.component import getUtility
#        from ldapadapter.interfaces import IManageableLDAPAdapter
#        from org.ict_ok.admin_utils.usermanagement.interfaces import IAdmUtilUserManagement
#        ldap = getUtility(ILDAPAuthentication,
#                          name='LDAPAuthentication')
#        pau=getUtility(IAdmUtilUserManagement)
#        pau.getPrincipal(u'principal.User')
#        pau.getPrincipal(u'LDAPAuthentication.demo')
#        ddd = ldap.authenticateCredentials({'login': 'demo', 'password': 'ddd'})
        subject = removeSecurityProxy(self.context.getSubject())
        subject_str = u', '.join([u"%s=%s" % (i_k, i_v)
                                for i_k, i_v in subject.get_components()])
        return subject_str

    def getValidNotBefore(self):
        timeString = removeSecurityProxy(self.getCertificate().get_notBefore())
        return datetime.strptime(\
                timeString, '%Y%m%d%H%M%SZ').replace(tzinfo=pytz.utc)

    def getValidNotAfter(self):
        #return self.getCertificate().get_notAfter()
        timeString = removeSecurityProxy(self.getCertificate().get_notAfter())
        return datetime.strptime(\
                timeString, '%Y%m%d%H%M%SZ').replace(tzinfo=pytz.utc)




class X509CertificateFolderDetails(CredentialFolderDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = CredentialFolderDetails.omit_viewfields + ['requirement']
    omit_addfields = CredentialFolderDetails.omit_addfields + ['requirement']
    omit_editfields = CredentialFolderDetails.omit_editfields + ['requirement']

# --------------- forms ------------------------------------


class DetailsX509CertificateForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of X.509 Certificate')
    factory = X509Certificate
    omitFields = X509CertificateDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)
    fields['ddd1'].widgetFactory = file.FileFieldWidget

class AddX509CertificateForm(AddComponentForm):
    """Add X.509 Certificate form"""
    label = _(u'Add X.509 Certificate')
    factory = X509Certificate
    attrInterface = IX509Certificate
    addInterface = IAddX509Certificate
    omitFields = X509CertificateDetails.omit_addfields
    _session_key = 'org.ict_ok.components.x509certificate'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = checkbox.SingleCheckBoxFieldWidget
    allFields['ddd1'].widgetFactory = file.FileFieldWidget


class EditX509CertificateForm(EditForm):
    """ Edit for X.509 Certificate """
    label = _(u'X.509 Certificate Edit Form')
    factory = X509Certificate
    omitFields = X509CertificateDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
    fields['ddd1'].widgetFactory = file.FileFieldWidget


class DeleteX509CertificateForm(DeleteForm):
    """ Delete the X.509 Certificate """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this X509Certificate: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IX509Certificate
    factory = X509Certificate
    factoryId = u'org.ict_ok.components.x509certificate.x509certificate.X509Certificate'
    allFields = fieldsForInterface(attrInterface, [])

#def getRoom(item, formatter):
#    if item.device is not None:
#        return item.device.room
#    return None

class Overview(SuperOverview):
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Health'),
                     getter=getHealth),
        IctGetterColumn(title=_('Title'),
                        getter=getTitle,
                        cell_formatter=link('overview.html')),
#        IctGetterColumn(title=_('Device'),
#                        getter=lambda i,f: i.device,
#                        cell_formatter=link('details.html')),
#        IctGetterColumn(title=_('Room'),
#                        getter=getRoom,
#                        cell_formatter=link('details.html')),
        DateGetterColumn(title=_('Modified'),
                        getter=getModifiedDate,
                        subsort=True,
                        cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    pos_column_index = 1
    sort_columns = [1, 2, 3, 4, 5]
