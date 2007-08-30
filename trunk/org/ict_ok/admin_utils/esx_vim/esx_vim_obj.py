# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""implementation of a "esx_vim daemon" 
"""

__version__ = "$Id$"

# phython imports
import time
import datetime
from pytz import timezone

# zope imports
from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from zope.app.container.contained import Contained
from zope.app.container.interfaces import IReadContainer

# ict_ok.org imports
from org.ict_ok.libs.lib import generateOid
from org.ict_ok.admin_utils.esx_vim.interfaces import IEsxVimObj
from org.ict_ok.admin_utils.esx_vim.esx_vim import globalEsxVimUtility

_ = MessageFactory('org.ict_ok')
utcTZ = timezone('UTC')
berlinTZ = timezone('Europe/Berlin')


class EsxVimObj(Contained):
    """ Base class for the esx vim objects """
    implements(IEsxVimObj, IReadContainer)
    
    def __init__(self):
        Contained.__init__(self)
        self.objectID = generateOid(self)
        self.name = None
        self.overallStatus = None
        self.localEsxUtil = None
        self.perlEsxObjRef = None
        
    def getObjectId(self):
        """
        get 'Universe ID' of object
        returns str
        """
        return self.objectID
    
    def eval_on_obj(self, eval_text='name()', fnct_args=None):
        """ evaluate an text with optional arguments on this object """
        if self.localEsxUtil is None:
            return None
        utilOId = self.localEsxUtil.getObjectId()
        myParams = {\
            'admUtilEsxVim': self.localEsxUtil,
            'cmd': 'eval_on_obj',
            'perlRef': self.perlEsxObjRef,
            'eval_text': eval_text,
            'fnct_args': fnct_args,
            }
        globalEsxVimUtility.esxThread.getQueue(\
            utilOId)['in'].put(myParams, True, 15)
        globalEsxVimUtility.esxThread.getQueue(\
            utilOId)['in'].join()
        retValue = globalEsxVimUtility.esxThread.getQueue(\
            utilOId)['out'].get(True, 15)
        return retValue

    def esxtime2python(self, arg_time):
        """ convert time string from esx to python datetime """
        try:
            if arg_time is None:
                return None
            str_left = arg_time.split('.')[0]
            my_timestrct = time.strptime(str_left, '%Y-%m-%dT%H:%M:%S')
            my_datetime = datetime.datetime(\
                my_timestrct.tm_year, my_timestrct.tm_mon, my_timestrct.tm_mday,
                my_timestrct.tm_hour, my_timestrct.tm_min, my_timestrct.tm_sec)
            return my_datetime.replace(tzinfo=utcTZ).astimezone(berlinTZ)
        except Exception, err:
            return str(err)
