# -*- coding: utf-8 -*-
#
# [[[cog
#    import sys; sys.path.extend(['.'])
#    import props
#    import cog
#    cog.out("# Copyright (c) ")
#    for year in props.copyrights:
#        cog.out("%4d, " % year)
#    cog.outl()
#    for author in props.authors:
#       cog.outl("#               %s <%s>" % (author['name'], author['email']))
#    cog.out("%s" % props.filename ) ]]]
# Copyright (c) 2006, 2007, 
#               Markus Leist <leist@ikom-online.de>
# [[[end]]]
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
# [[[cog cog.outl('"""Interface of %(purpose)s"""' % props.__dict__)]]]
"""Interface of test util

the test util should demonstrate the use of cog
"""
# [[[end]]]
"""implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.dublincore.interfaces import IZopeDublinCore

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter

# z3c imports
from z3c.form import field
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
#[[[cog
#   cog.out("""\
#   from %(longpath_interface)s import \\
#        I%(utilityname)s
#   """ % props.__dict__, dedent=True)
#]]]
from org.ict_ok.admin_utils.testmod.interfaces import \
     IAdmUtilTestMod
#[[[end]]]
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


#[[[cog
#   cog.out("""\
#   class %(utilityname)sDetails(SupernodeDetails):
#       \"\"\"%(utilitytitle)s
#       \"\"\"
#       
#       omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
#       omit_editfields = SupernodeDetails.omit_editfields + ['ikName']
#   """ % props.__dict__, dedent=True)
#]]]
class AdmUtilTestModDetails(SupernodeDetails):
    """Test Utiltiy
    """
    
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']
#[[[end]]]



# --------------- forms ------------------------------------


#[[[cog
#   cog.out("""\
#   class Details%(utilityname)sForm(DisplayForm):
#       \"\"\" Display form for the object \"\"\"
#       
#       label = _(u'settings of %(modulename)s')
#       fields = field.Fields(I%(utilityname)s).omit(
#          *%(utilityname)sDetails.omit_viewfields)
#   """ % props.__dict__, dedent=True)
#]]]
class DetailsAdmUtilTestModForm(DisplayForm):
    """ Display form for the object """
    
    label = _(u'settings of TestMod')
    fields = field.Fields(IAdmUtilTestMod).omit(
       *AdmUtilTestModDetails.omit_viewfields)
#[[[end]]]


#[[[cog
#   cog.out("""\
#   class Edit%(utilityname)sForm(EditForm):
#       \"\"\" Display form for the object \"\"\"
#       
#       label = _(u'edit %(modulename)s properties')
#       fields = field.Fields(I%(utilityname)s).omit(
#          *%(utilityname)sDetails.omit_editfields)
#   """ % props.__dict__, dedent=True)
#]]]
class EditAdmUtilTestModForm(EditForm):
    """ Display form for the object """
    
    label = _(u'edit  TestMod properties')
    fields = field.Fields(IAdmUtilTestMod).omit(
       *AdmUtilTestModDetails.omit_editfields)
#[[[end]]]
