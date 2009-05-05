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
from zope.i18n import translate

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.components.component import Component
from org.ict_ok.components.supernode.adapter.rpt_pdf import \
     RptPdf as ParentRptPdf
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf


class RptPdf(ParentRptPdf):
    """adapter implementation of credential instance -> PDF Report
    """

    implements(IRptPdf)
    adapts(IComponent)
    factory = Component
    omitFields = ParentRptPdf.omitFields + ['isTemplate', 'requirements']

    def prependAttributeTable(self):
        data = ParentRptPdf.prependAttributeTable(self)
        if self.context.isTemplate:
            namePara = self._convertNamePara(u'')
            textTransl = translate(u'Object is template',
                                   domain='org.ict_ok',
                                   context=self.request)
            valPara = self._convertValPara(u'<b>%s</b><br />' % textTransl)
            data.append([namePara, valPara])
            data.append([u'', u''])
        return data
