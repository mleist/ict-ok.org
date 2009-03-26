# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of X509Certificate"""

__version__ = "$Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# python imports
from OpenSSL import crypto

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.folder import Folder

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.credential.credential import Credential
from org.ict_ok.components.x509certificate.interfaces import \
    IX509Certificate, IX509CertificateFolder, IAddX509Certificate
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import Component
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents


class X509Certificate(Credential):
    """
    the template instance
    """
    implements(IX509Certificate)
    shortName = "x509certificate"
    
    publicKey = FieldProperty(IX509Certificate['publicKey'])
    
    fullTextSearchFields = []
    fullTextSearchFields.extend(Credential.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Credential.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(X509Certificate)
        for (name, value) in data.items():
            if name in IX509Certificate.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        Credential.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(X509Certificate)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)

    def __getCertificate__(self):
        return crypto.load_certificate(crypto.FILETYPE_PEM, self.publicKey)

    #>>> dir(co)
    #['add_extensions', 'digest', 'get_issuer', 'get_notAfter', 'get_notBefore',
    # 'get_pubkey', 'get_serial_number', 'get_subject', 'get_version',
    # 'gmtime_adj_notAfter', 'gmtime_adj_notBefore', 'has_expired', 
    # 'set_issuer', 'set_notAfter', 'set_notBefore', 'set_pubkey', 
    # 'set_serial_number', 'set_subject', 'set_version', 'sign', 'subject_name_hash']

    def getIssuerName(self):
        return unicode(self.__getCertificate__().get_issuer())

    def getSubject(self):
        return unicode(self.__getCertificate__().get_subject())

    def getSerialNumber(self):
        return self.__getCertificate__().get_serial_number()

    def getSignatureAlgorithm(self):
        return self.__getCertificate__().get_pubkey().bits()

    def getPublicKeyAlgorithm(self):
        return self.__getCertificate__().get_pubkey().bits()

    def getPublicKeySize(self):
        return self.__getCertificate__().get_pubkey().bits()

    def getVersion(self):
        return self.__getCertificate__().get_version()

    def getValidNotBefore(self):
        return self.__getCertificate__().get_notBefore()

    def getValidNotAfter(self):
        return self.__getCertificate__().get_notAfter()







class X509CertificateFolder(Superclass, Folder):
    implements(IX509CertificateFolder,
               IImportCsvData,
               IImportXlsData,
               IAddX509Certificate)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
