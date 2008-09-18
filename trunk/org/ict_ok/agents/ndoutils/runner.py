# -*- coding: utf-8 -*-
#
# Copyright (c) 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0621,W0212
#
"""Cron runner based on gocept.runner
"""

__version__ = "$Id$"

# python imports
import transaction
import gocept.runner


# zope imports
from zope.app.appsetup.bootstrap import getInformationFromEvent

# ict_ok.org imports
from org.ict_ok.version import getIkVersion
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor

def bootStrapSubscriber(event):
    """ log the startup to our supervisor
    """
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    sitem = root_folder.getSiteManager()
    utils = [ util for util in sitem.registeredUtilities()
              if util.provided.isOrExtends(IAdmUtilSupervisor)]
    instAdmUtilSupervisor = utils[0].component
    instAdmUtilSupervisor.appendEventHistory(\
        u"'ndo runner' started (Vers. %s) (%d bytes) (%d objects)" \
        % (getIkVersion(), dummy_db.getSize(), dummy_db.objectCount()))
    transaction.get().commit()
    connection.close()


class NdoMain(gocept.runner.appmain):
    """entry point functions for main loops and ndo thread.
    """
    def __init__(self, ticks=1, principal=None):
        print "ndomain.__init__"
        #import traceback
        #traceback.print_stack()
        # start ndo thread here
        # ...
        gocept.runner.appmain.__init__(self, ticks, principal)


@NdoMain(ticks=1.0, principal='zope.mgr')
def runner():
    """ this function will run every second
    """
    # import in this context
    import zope.app.component.hooks
    import zope.security.management
    import zope.app.appsetup.product
    from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor
    site = zope.app.component.hooks.getSite()
    sitemgr = site.getSiteManager()
    admSupervisor = sitemgr.getUtility(IAdmUtilSupervisor)
    print "admSupervisor: ", admSupervisor
