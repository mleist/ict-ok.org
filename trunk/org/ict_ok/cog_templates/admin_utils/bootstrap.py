# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
# [[[cog
#    import props
#    uname_len = len(props.utilityname)
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
# pylint: disable-msg=E1101
#
# [[[cog cog.outl('"""%s"""' % props.purpose)]]]
"""test util

the test util should demonstrate the use of cog
"""
# [[[end]]]

__version__ = "$Id$"

# phython imports
import logging
import transaction
from datetime import datetime

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.appsetup.bootstrap import ensureUtility
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.app.component.interfaces import ISite
from zope.app.container.interfaces import IContainer

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
#[[[cog
#   cog.out("""\
#   from %(longpath_interface)s import \\
#        I%(utilityname)s
#   from %(longpath_file)s import \\
#        %(utilityname)s
#   """ % props.__dict__, dedent=True)
#]]]
from org.ict_ok.admin_utils.testmod.interfaces import \
     IAdmUtilTestMod
from org.ict_ok.admin_utils.testmod.testmod import \
     AdmUtilTestMod
#[[[end]]]

#[[[cog cog.outl('logger = logging.getLogger(%s)' % props.loggername)]]]
logger = logging.getLogger(AdmUtilTestMod)
#[[[end]]]

def bootStrapSubscriberDatabase(event):
    """initialisation of eventcrossbar utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    #[[[cog
    #   cog.out("""\
    #   made%(utilityname)s = ensureUtility(root_folder, I%(utilityname)s,
    #                                      '%(utilityname)s', %(utilityname)s, '',
    #                                      copy_to_zlog=False, asObject=True)
    #   """ % props.__dict__, dedent=True)
    #]]]
    madeAdmUtilTestMod = ensureUtility(root_folder, IAdmUtilTestMod,
                                       'AdmUtilTestMod', AdmUtilTestMod, '',
                                       copy_to_zlog=False, asObject=True)
    #[[[end]]]

    #[[[cog
    #   cog.out("""\
    #   if isinstance(made%(utilityname)s, %(utilityname)s):
    #       logger.info(u"bootstrap: Ensure named %(utilityname)s")
    #       dcore = IWriteZopeDublinCore(made%(utilityname)s)
    #       dcore.title = u"%(utilitytitle)s"
    #       dcore.created = datetime.utcnow()
    #       made%(utilityname)s.ikName = dcore.title
    #       made%(utilityname)s.__post_init__()
    #       sitem = root_folder.getSiteManager()
    #       utils = [util for util in sitem.registeredUtilities()
    #                if util.provided.isOrExtends(IAdmUtilSupervisor)]
    #       instAdmUtilSupervisor = utils[0].component
    #       instAdmUtilSupervisor.appendEventHistory(\\
    #           u" bootstrap: made %(utilitytitle)s")
    #   """ % props.__dict__, dedent=True)
    #]]]
    if isinstance(madeAdmUtilTestMod, AdmUtilTestMod):
        logger.info(u"bootstrap: Ensure named AdmUtilTestMod")
        dcore = IWriteZopeDublinCore(madeAdmUtilTestMod)
        dcore.title = u"Test Utiltiy"
        dcore.created = datetime.utcnow()
        madeAdmUtilTestMod.ikName = dcore.title
        madeAdmUtilTestMod.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [util for util in sitem.registeredUtilities()
                 if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made Test Utiltiy")
    #[[[end]]]

    transaction.get().commit()
    connection.close()
