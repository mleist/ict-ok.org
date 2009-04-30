# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,E0211,W0232
#
"""Interface of X509Certificate"""


__version__ = "$Id$"

#python imports
from OpenSSL import crypto

# zope imports
from zope.interface import Interface
from zope.interface import Attribute, Invalid, invariant
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Date, Int, Text

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IX509Certificate(Interface):
    """A X509Certificate object."""
    publicKey = Text(
        max_length = 4000,
        title = _("public key (PEM)"),
        description = _("The PEM-encoded raw public key."),
        required = True)

    @invariant
    def ensureValidPublicKey(obj_x509):
        """publicKey must be valid PEM string
        """
        try:
            crypto.load_certificate(crypto.FILETYPE_PEM, obj_x509.publicKey)
        except crypto.Error, errText:
            raise Invalid(u'Invalid public key: %s' % errText)

    def getCertificate():
        """get certificate data
        """
        
    def getIssuerName():
        """get some certificate data
        """

    def getSubject():
        """get some certificate data
        """

    def getSerialNumber():
        """get some certificate data
        """

    def getPublicKeySize():
        """get some certificate data
        """

    def getVersion():
        """get some certificate data
        """

    def getRawValidNotBefore():
        """get some certificate data
        """

    def getRawValidNotAfter():
        """get some certificate data
        """

    def validNotBefore():
        """get some certificate data
        """

    def validNotAfter():
        """get some certificate data
        """


class IX509CertificateFolder(Interface):
    """Container for PersonalComputer objects
    """


class IAddX509Certificate(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllX509CertificateTemplates",
        required = False)
