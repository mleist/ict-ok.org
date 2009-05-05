# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of X509Certificate"""

__version__ = "$Id$"

# python imports
from OpenSSL import crypto
from datetime import datetime
import pytz

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

def AllX509CertificateTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IX509Certificate)

def AllX509Certificates(dummy_context):
    return AllComponents(dummy_context, IX509Certificate)


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

    def getCertificate(self):
        return crypto.load_certificate(crypto.FILETYPE_PEM,
                                            self.publicKey)

    #>>> dir(co)
    #['add_extensions', 'digest', 'get_issuer', 'get_notAfter', 'get_notBefore',
    # 'get_pubkey', 'get_serial_number', 'get_subject', 'get_version',
    # 'gmtime_adj_notAfter', 'gmtime_adj_notBefore', 'has_expired', 
    # 'set_issuer', 'set_notAfter', 'set_notBefore', 'set_pubkey', 
    # 'set_serial_number', 'set_subject', 'set_version', 'sign', 'subject_name_hash']

    def getIssuerName(self):
        return self.getCertificate().get_issuer()

    def getSubject(self):
        return self.getCertificate().get_subject()

    def getSerialNumber(self):
        return self.getCertificate().get_serial_number()

    def getPublicKeySize(self):
        return self.getCertificate().get_pubkey().bits()

    def getVersion(self):
        return self.getCertificate().get_version()

    def getRawValidNotBefore(self):
        return self.getCertificate().get_notBefore()
        
#    def getValidNotBefore(self):
#        timeString = self.getRawValidNotBefore()
#        return datetime.strptime(\
#                timeString, '%Y%m%d%H%M%SZ').replace(tzinfo=pytz.utc)

    def getRawValidNotAfter(self):
        return self.getCertificate().get_notAfter()
        
#    def getValidNotAfter(self):
#        #return self.getCertificate().get_notAfter()
#        timeString = self.getRawValidNotAfter()
#        return datetime.strptime(\
#                timeString, '%Y%m%d%H%M%SZ').replace(tzinfo=pytz.utc)

    @property
    def validNotBefore(self):
        timeString = self.getRawValidNotBefore()
        return datetime.strptime(\
                timeString, '%Y%m%d%H%M%SZ').replace(tzinfo=pytz.utc)
    
    @property
    def validNotAfter(self):
        timeString = self.getRawValidNotAfter()
        return datetime.strptime(\
                timeString, '%Y%m%d%H%M%SZ').replace(tzinfo=pytz.utc)






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
