# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0613,W0232,W0201,W0142,W0107
#
"""implementation of browser class of IkSite object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# zc imports

# ict-ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm, AddForm, DeleteForm
from org.ict_ok.components.superclass.browser.superclass import \
     Overview as SuperclassOverview
from org.ict_ok.components.superclass.browser.superclass import \
     GetterColumn, getStateIcon, getTitle, raw_cell_formatter, \
     link, getModifiedDate, getActionBottons
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.admin_utils.idchooser.idchooser_util import AdmUtilIdChooser

_ = MessageFactory('org.ict_ok')


def getTitle(item, formatter):
    """
    Titel for Overview
    """
    try:
        return IBrwsOverview(item).getTitle()
    except TypeError:
        return str(item.__class__.__name__)

# --------------- menu entries -----------------------------


# --------------- object details ---------------------------


class AdmUtilIdChooserDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    
class Overview(SuperclassOverview):
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Title'),
                     getter=getTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(_('Counter'), lambda i,f: i.counter),
        GetterColumn(_('Step'), lambda i,f: i.step),
        GetterColumn(title=_('Modified'),
                     getter=getModifiedDate,
                     subsort=True,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    pos_column_index = 1
    sort_columns = [1, 2, 3, 4]
    #sort_columns = [0]
# --------------- forms ------------------------------------

# ------ Categories

class DetailsAdmUtilIdChooserForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of categories')
    factory = AdmUtilIdChooser
    omitFields = AdmUtilIdChooserDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

