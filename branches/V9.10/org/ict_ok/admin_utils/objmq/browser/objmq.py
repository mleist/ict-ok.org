# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=E1101,E0611,W0232,W0142,R0901
#
"""implementation of browser class of Object-Message-Queue-Utility
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.objmq.objmq import AdmUtilObjMQ

_ = MessageFactory('org.ict_ok')


class AdmUtilObjMQDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']


# --------------- forms ------------------------------------


class ViewAdmUtilObjMQForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of object message queue')
    factory = AdmUtilObjMQ
    omitFields = AdmUtilObjMQDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class EditAdmUtilObjMQForm(EditForm):
    """ Edit for for net """
    label = _(u'edit object message queue')
    factory = AdmUtilObjMQ
    omitFields = AdmUtilObjMQDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
