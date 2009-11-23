# -*- coding: utf-8 -*-
#
# [[[cog
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
# pylint: disable-msg=E0213,W0232,W0622
#
# [[[cog cog.outl('"""Interface of %(purpose)s"""' % props.__dict__)]]]
"""Interface of test util

the test util should demonstrate the use of cog
"""
# [[[end]]]

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


#[[[cog
#   cog.out("""\
#   class I%(utilityname)s(ISupernode):
#       \"\"\"%(utilitytitle)s
#       \"\"\"
#   """ % props.__dict__, dedent=True)
#]]]
class IAdmUtilTestMod(ISupernode):
    """Test Utiltiy
    """
#[[[end]]]
