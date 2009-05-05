# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""Adapter implementation for generating pdf reports of Outlet"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.x509certificate.interfaces import \
    IX509Certificate
from org.ict_ok.components.x509certificate.x509certificate import \
    X509Certificate
from org.ict_ok.components.x509certificate.browser.x509certificate import \
    X509CertificateDetails
from org.ict_ok.components.credential.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of An network outlet instance -> PDF Report
    """

    implements(IRptPdf)
    adapts(IX509Certificate)
    factory = X509Certificate
    omitFields = ParentRptPdf.omitFields + ['publicKey']

    def appendAttributeTable(self):
        data = []
        my_formatter = self.request.locale.dates.getFormatter(
            'dateTime', 'full')
        x509CertificateDetails = X509CertificateDetails()
        x509CertificateDetails.context = self.context
        # subject
        namePara = self._convertNamePara(u'X.509 subject')
        valPara = self._convertValPara(x509CertificateDetails.getSubject())
        data.append([namePara, valPara])
        # issuer name
        namePara = self._convertNamePara(u'X.509 issuer name')
        valPara = self._convertValPara(x509CertificateDetails.getIssuerName())
        data.append([namePara, valPara])
        # serial number
        namePara = self._convertNamePara(u'X.509 serial number')
        valPara = self._convertValPara(u"%d<sub>10</sub> / %X<sub>16</sub>" % \
                           (self.context.getSerialNumber(),
                            self.context.getSerialNumber()))
        data.append([namePara, valPara])
        # key size
        namePara = self._convertNamePara(u'Public key size')
        valPara = self._convertValPara(\
            u'%s bit' % self.context.getPublicKeySize())
        data.append([namePara, valPara])
        # version
        namePara = self._convertNamePara(u'X.509 version')
        valPara = self._convertValPara(self.context.getVersion())
        data.append([namePara, valPara])
        # valid not before
        namePara = self._convertNamePara(u'X.509 valid not before')
        valPara = self._convertValPara(\
            my_formatter.format(self.context.validNotBefore))
        data.append([namePara, valPara])
        # valid not after
        namePara = self._convertNamePara(u'X.509 valid not after')
        valPara = self._convertValPara(\
            my_formatter.format(self.context.validNotAfter))
        data.append([namePara, valPara])
        return data
