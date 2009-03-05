# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of PhysicalComponent"""

__version__ = "$Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.schema import vocabulary
from zope.app.pagetemplate.urlquote import URLQuote

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.components.physical_component.interfaces import IPhysicalComponent
from org.ict_ok.components.physical_component.physical_component import PhysicalComponent
from org.ict_ok.components.browser.component import ComponentDetails

_ = MessageFactory('org.ict_ok')


# --------------- helper functions -------------------------

def vocabValue(vocabName=None, token=None, request=None):
    if vocabName is None:
        return None
    if token is None:
        return None
    vocabReg = vocabulary.getVocabularyRegistry()
    if vocabReg is not None:
        vocab = vocabReg.get(request, vocabName)
        if vocab is not None:
            vocabTerm = vocab.getTerm(token)
            if vocabTerm:
                return vocabTerm.title
    return None

def getUserName(item, formatter):
    """
    Titel for Overview
    """
    username = vocabValue('AllLdapUser', item.user, formatter.request)
    if username:
        return username
    else:
        return u''

def fsearch_user_formatter(value, item, formatter):
    username = vocabValue('AllLdapUser', item.user, formatter.request)
    if username:
        quoter = URLQuote(item.user)
        return u'<a href="/@@fsearch?key=%s">%s</a>' % (quoter.quote(), username)
    else:
        return u''


# --------------- object details ---------------------------


class PhysicalComponentDetails(ComponentDetails):
    """ Class for PhysicalComponent details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class PhysicalComponentFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
