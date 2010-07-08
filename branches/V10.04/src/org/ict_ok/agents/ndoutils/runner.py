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
import gocept.runner

# zope imports
from zope.app.catalog.interfaces import ICatalog

# ict_ok.org imports
from org.ict_ok.libs.iklogger import IkLogger
from org.ict_ok.libs.ikqueue import IkQueue
from org.ict_ok.version import getVersRevision
from org.ict_ok.agents.ndoutils.ndo_thread import NdoThread

__version__ = "$Id$"

ndo_data_types = {
    "100": "NDO_API_LOGENTRY",
    "200": "NDO_API_PROCESSDATA",
    "201": "NDO_API_TIMEDEVENTDATA",
    "202": "NDO_API_LOGDATA",
    "203": "NDO_API_SYSTEMCOMMANDDATA",
    "204": "NDO_API_EVENTHANDLERDATA",
    "205": "NDO_API_NOTIFICATIONDATA",
    "206": "NDO_API_SERVICECHECKDATA",
    "207": "NDO_API_HOSTCHECKDATA",
    "208": "NDO_API_COMMENTDATA",
    "209": "NDO_API_DOWNTIMEDATA",
    "210": "NDO_API_FLAPPINGDATA",
    "211": "NDO_API_PROGRAMSTATUSDATA",
    "212": "NDO_API_HOSTSTATUSDATA",
    "213": "NDO_API_SERVICESTATUSDATA",
    "214": "NDO_API_ADAPTIVEPROGRAMDATA",
    "215": "NDO_API_ADAPTIVEHOSTDATA",
    "216": "NDO_API_ADAPTIVESERVICEDATA",
    "217": "NDO_API_EXTERNALCOMMANDDATA",
    "218": "NDO_API_AGGREGATEDSTATUSDATA",
    "219": "NDO_API_RETENTIONDATA",
    "220": "NDO_API_CONTACTNOTIFICATIONDATA",
    "221": "NDO_API_CONTACTNOTIFICATIONMETHODDATA",
    "222": "NDO_API_ACKNOWLEDGEMENTDATA",
    "223": "NDO_API_STATECHANGEDATA",
    "224": "NDO_API_CONTACTSTATUSDATA",
    "225": "NDO_API_ADAPTIVECONTACTDATA",
    "300": "NDO_API_MAINCONFIGFILEVARIABLES",
    "301": "NDO_API_RESOURCECONFIGFILEVARIABLES",
    "302": "NDO_API_CONFIGVARIABLES",
    "303": "NDO_API_RUNTIMEVARIABLES",
    "400": "NDO_API_HOSTDEFINITION",
    "401": "NDO_API_HOSTGROUPDEFINITION",
    "402": "NDO_API_SERVICEDEFINITION",
    "403": "NDO_API_SERVICEGROUPDEFINITION",
    "404": "NDO_API_HOSTDEPENDENCYDEFINITION",
    "405": "NDO_API_SERVICEDEPENDENCYDEFINITION",
    "406": "NDO_API_HOSTESCALATIONDEFINITION",
    "407": "NDO_API_SERVICEESCALATIONDEFINITION",
    "408": "NDO_API_COMMANDDEFINITION",
    "409": "NDO_API_TIMEPERIODDEFINITION",
    "410": "NDO_API_CONTACTDEFINITION",
    "411": "NDO_API_CONTACTGROUPDEFINITION",
    "412": "NDO_API_HOSTEXTINFODEFINITION",
    "413": "NDO_API_SERVICEEXTINFODEFINITION",
}

ndo_event_types = {
    "1" : "NEBTYPE_HELLO",
    "2" : "NEBTYPE_GOODBYE",
    "3" : "NEBTYPE_INFO",
    "100" : "NEBTYPE_PROCESS_START",
    "101" : "NEBTYPE_PROCESS_DAEMONIZE",
    "102" : "NEBTYPE_PROCESS_RESTART",
    "103" : "NEBTYPE_PROCESS_SHUTDOWN",
    "104" : "NEBTYPE_PROCESS_PRELAUNCH",
    "105" : "NEBTYPE_PROCESS_EVENTLOOPSTART",
    "106" : "NEBTYPE_PROCESS_EVENTLOOPEND",
    "200" : "NEBTYPE_TIMEDEVENT_ADD",
    "201" : "NEBTYPE_TIMEDEVENT_REMOVE",
    "202" : "NEBTYPE_TIMEDEVENT_EXECUTE",
    "203" : "NEBTYPE_TIMEDEVENT_DELAY",
    "204" : "NEBTYPE_TIMEDEVENT_SKIP",
    "205" : "NEBTYPE_TIMEDEVENT_SLEEP",
    "300" : "NEBTYPE_LOG_DATA",
    "301" : "NEBTYPE_LOG_ROTATION",
    "400" : "NEBTYPE_SYSTEM_COMMAND_START",
    "401" : "NEBTYPE_SYSTEM_COMMAND_END",
    "500" : "NEBTYPE_EVENTHANDLER_START",
    "501" : "NEBTYPE_EVENTHANDLER_END",
    "600" : "NEBTYPE_NOTIFICATION_START",
    "601" : "NEBTYPE_NOTIFICATION_END",
    "602" : "NEBTYPE_CONTACTNOTIFICATION_START",
    "603" : "NEBTYPE_CONTACTNOTIFICATION_END",
    "604" : "NEBTYPE_CONTACTNOTIFICATIONMETHOD_START",
    "605" : "NEBTYPE_CONTACTNOTIFICATIONMETHOD_END",
    "700" : "NEBTYPE_SERVICECHECK_INITIATE",
    "701" : "NEBTYPE_SERVICECHECK_PROCESSED",
    "702" : "NEBTYPE_SERVICECHECK_RAW_START",
    "703" : "NEBTYPE_SERVICECHECK_RAW_END",
    "704" : "NEBTYPE_SERVICECHECK_ASYNC_PRECHECK",
    "800" : "NEBTYPE_HOSTCHECK_INITIATE",
    "801" : "NEBTYPE_HOSTCHECK_PROCESSED",
    "802" : "NEBTYPE_HOSTCHECK_RAW_START",
    "803" : "NEBTYPE_HOSTCHECK_RAW_END",
    "804" : "NEBTYPE_HOSTCHECK_ASYNC_PRECHECK",
    "805" : "NEBTYPE_HOSTCHECK_SYNC_PRECHECK",
    "900" : "NEBTYPE_COMMENT_ADD",
    "901" : "NEBTYPE_COMMENT_DELETE",
    "902" : "NEBTYPE_COMMENT_LOAD",
    "1000" : "NEBTYPE_FLAPPING_START",
    "1001" : "NEBTYPE_FLAPPING_STOP",
    "1100" : "NEBTYPE_DOWNTIME_ADD",
    "1101" : "NEBTYPE_DOWNTIME_DELETE",
    "1102" : "NEBTYPE_DOWNTIME_LOAD",
    "1103" : "NEBTYPE_DOWNTIME_START",
    "1104" : "NEBTYPE_DOWNTIME_STOP",
    "1200" : "NEBTYPE_PROGRAMSTATUS_UPDATE",
    "1201" : "NEBTYPE_HOSTSTATUS_UPDATE",
    "1202" : "NEBTYPE_SERVICESTATUS_UPDATE",
    "1203" : "NEBTYPE_CONTACTSTATUS_UPDATE",
    "1300" : "NEBTYPE_ADAPTIVEPROGRAM_UPDATE",
    "1301" : "NEBTYPE_ADAPTIVEHOST_UPDATE",
    "1302" : "NEBTYPE_ADAPTIVESERVICE_UPDATE",
    "1303" : "NEBTYPE_ADAPTIVECONTACT_UPDATE",
    "1400" : "NEBTYPE_EXTERNALCOMMAND_START",
    "1401" : "NEBTYPE_EXTERNALCOMMAND_END",
    "1500" : "NEBTYPE_AGGREGATEDSTATUS_STARTDUMP",
    "1501" : "NEBTYPE_AGGREGATEDSTATUS_ENDDUMP",
    "1600" : "NEBTYPE_RETENTIONDATA_STARTLOAD",
    "1601" : "NEBTYPE_RETENTIONDATA_ENDLOAD",
    "1602" : "NEBTYPE_RETENTIONDATA_STARTSAVE",
    "1603" : "NEBTYPE_RETENTIONDATA_ENDSAVE",
    "1700" : "NEBTYPE_ACKNOWLEDGEMENT_ADD",
    "1701" : "NEBTYPE_ACKNOWLEDGEMENT_REMOVE",
    "1702" : "NEBTYPE_ACKNOWLEDGEMENT_LOAD",
    "1800" : "NEBTYPE_STATECHANGE_START",
    "1801" : "NEBTYPE_STATECHANGE_END"
}

def triggerNdoEvent(arg_dict, sitemgr):
    """
    """
    print "triggerNdoEvent                              <-----------------"
    import pprint
    pprint.pprint(arg_dict)
    #if arg_dict.has_key('114') and arg_dict['114'] == "1234567890as" \
    if False and \
       (arg_dict.has_key('1')) and \
       (arg_dict['1'] in ["701", "801"]) and \
       (arg_dict['99999'] in ["206", "207", "210"]):
        try:
            print "ndo_data_types: %s (%s)" % \
                  (ndo_data_types[arg_dict['99999']], arg_dict['99999'])
        except:
            print "ndo_data_types: (%s)" % \
                  (arg_dict['99999'])
        try:
            print "ndo_event_types: %s (%s)" % \
                  (ndo_event_types[arg_dict['1']], arg_dict['1'])
        except:
            print "ndo_event_types: (%s)" % \
                  (arg_dict['1'])
        try:
            print "    ('4': %s  [NDO_DATA_TIMESTAMP])" % \
                  datetime.fromtimestamp(float(arg_dict['4']), berlinTZ)
        except:
            pass
        try:
            print "    ('11': %s  [NDO_DATA_CHECKCOMMAND])" % \
                  (arg_dict['11'])
        except:
            pass
        try:
            print "    ('14': %s  [NDO_DATA_COMMANDLINE])" % \
                  (arg_dict['14'])
        except:
            pass
        try:
            print "    ('19': %s  [NDO_DATA_COMMENTTIME])" % \
                  datetime.fromtimestamp(float(arg_dict['19']), berlinTZ)
        except:
            pass
        try:
            print "    ('25': %s  [NDO_DATA_CURRENTCHECKATTEMPT])" % \
                  (arg_dict['25'])
        except:
            pass
        try:
            print "    ('33': %s  [NDO_DATA_ENDTIME])" % \
                  (arg_dict['33'])
        except:
            pass
        try:
            print "    ('42': %s  [NDO_DATA_EXECUTIONTIME])" % \
                  (arg_dict['42'])
        except:
            pass
        try:
            print "    ('48': %s  [NDO_DATA_FLAPPINGTYPE])" % \
                  (arg_dict['48'])
        except:
            pass
        try:
            print "    ('52': %s  [NDO_DATA_HIGHTHRESHOLD])" % \
                  (arg_dict['52'])
        except:
            pass
        try:
            print "    ('53': %s  [NDO_DATA_HOST])" % (arg_dict['53'])
        except:
            pass
        try:
            print "    ('55': %s  [NDO_DATA_LASTCOMMANDCHECK])" % \
                  datetime.fromtimestamp(float(arg_dict['55']), berlinTZ)
        except:
            pass
        try:
            print "    ('75': %s  [NDO_DATA_LOWTHRESHOLD])" % \
                  (arg_dict['75'])
        except:
            pass
        try:
            print "    ('95': %s  [NDO_DATA_OUTPUT])" % (arg_dict['95'])
        except:
            pass
        try:
            print "    ('98': %s  [NDO_DATA_PERCENTSTATECHANGE])" % \
                  (arg_dict['98'])
        except:
            pass
        try:
            print "    ('110': %s  [NDO_DATA_RETURNCODE])" % \
                  (arg_dict['110'])
        except:
            pass
        try:
            print "    ('114': %s  [NDO_DATA_SERVICE])" % \
                  (arg_dict['114'])
        except:
            pass
        try:
            print "    ('118': %s  [NDO_DATA_STATE])" % \
                  (arg_dict['118'])
        except:
            pass
        try:
            print "    ('121': %s  [NDO_DATA_STATETYPE])" % \
                  (arg_dict['121'])
        except:
            pass
        print "dict: %s" % arg_dict
    
    #print "arg_dict: %s" % arg_dict
    #globalNagiosUtility.lastSeen(arg_dict)

    ##ndo_event_types: NEBTYPE_HOSTCHECK_PROCESSED (801)
    ##('4': 2007-04-29 06:26:07.951900+02:00  [NDO_DATA_TIMESTAMP])
    ##('14':   [NDO_DATA_COMMANDLINE])
    ##('25': 1  [NDO_DATA_CURRENTCHECKATTEMPT])
    ##('33': 1177820767.9512  [NDO_DATA_ENDTIME])
    ##('42': 4.06045  [NDO_DATA_EXECUTIONTIME])
    ##('53': 738eda44bafba017120992a2af649fe4e  [NDO_DATA_HOST])
    ##('95': PING OK - Packet loss = 0%, RTA = 0.38 ms  [NDO_DATA_OUTPUT])
    ##('110': 0  [NDO_DATA_RETURNCODE])
    ##('118': 0  [NDO_DATA_STATE])
    ##('121': 1  [NDO_DATA_STATETYPE])

    # with new nagios
    #'99999': '207',
    #'99997': 45,
    #'117': '1205935461.56343',
    #'110': '0',
    #'118': '1',
    #'25': '1',
    #'42': '0.00000',
    #'1': '800',
    #'3': '0',
    #'2': '0',
    #'4': '1205935461.56538',
    #'99': '', 
    #'121': '1', 
    #'123': '30',
    #'71': '0.05600', 
    #'127': 'check-host-alive', 
    #'95': '', 
    #'13': '', 
    #'12': '0', 
    #'14': '/opt/nagios/libexec/check_ping -H 172.16.64.210 -w 3000.0,80% -c 5000.0,100% -p 5', 
    #'76': '10', 
    #'33': '0.0', 
    #'32': '0', 
    #'53': 'windschrott'}

    #my_catalog = zapi.getUtility(ICatalog)
    #if (arg_dict.has_key('1')) and \
       #(arg_dict['1'] in ["801"]) and \
       #(arg_dict['99999'] in ["207"]):
        #res = my_catalog.searchResults(oid_index=arg_dict['53'])
        #if len(res) > 0:
            #hostObj = iter(res).next()
            ##print "hostObj: %s" % hostObj
            #if arg_dict['118'] == "0":
                #hostObj.trigger_online()
            #elif arg_dict['118'] == "1":
                #hostObj.trigger_offline()
            #elif arg_dict['118'] == "2":
                #hostObj.trigger_not1()
            #else:
                #pass

    my_catalog = sitemgr.getUtility(ICatalog)
    if (arg_dict.has_key('1')) and \
       (arg_dict['1'] in ["801"]) and \
       (arg_dict['99999'] in ["207"]):
        res = my_catalog.searchResults(oid_index=arg_dict['53'])
        if len(res) > 0:
            hostObj = iter(res).next()
            if arg_dict['118'] == "0":
                hostObj.trigger_online()
            elif arg_dict['118'] == "1":
                hostObj.trigger_offline()
            elif arg_dict['118'] == "2":
                hostObj.trigger_not1()
            else:
                pass

    
    
    ##'99999': '200', '99997': 1058, '1': '104', '3': '0', '2': '0', '4': '1177680803.736697', '102': '17170', '107': '3.0a3', '104': '04-10-2007', '105': 'Nagios'}
    ##'99999': '200', '99997': 1059, '1': '100', '3': '0', '2': '0', '4': '1177680803.743882', '102': '17170', '107': '3.0a3', '104': '04-10-2007', '105': 'Nagios'}
    ##'99999': '408', '127': 'check_hpjd', '4': '1177680803.758473', '99997': 1087, '14': '$USER1$/check_hpjd -H $HOSTADDRESS$ $ARG1$'
    #if arg_dict['99999'] == '408': # NDO_API_COMMANDDEFINITION
        #globalNagiosUtility.setCommandDefinition(arg_dict)
        ## 127: NDO_DATA_COMMANDNAME
    ##'99999': '213', '113': '0', '37': '', '98': '0.00000', '115': '1', '114': 'ssh Server', '62': '0', '63': '1177681797', '64': '0', '66': '1177681797', '67': '0', '83': '1177682097', '80': '0', '86': '5.000000', '84': '0', '85': '0', '25': '1', '26': '0', '27': '0', '47': '1', '45': '1', '42': '0.20843', '1': '1202', '3': '0', '2': '0', '4': '1177681807.192778', '7': '0', '9': '1', '209': '24x7', '99': '', '76': '3', '38': '1', '99997': 1718, '71': '0.59300', '70': '0', '103': '1', '93': '0', '101': '0', '95': 'SSH OK - OpenSSH_4.2p1 Debian-7ubuntu3.1 (protocol 2.0)', '97': '1', '11': 'check_ssh', '12': '0', '121': '1', '61': '1177681797', '54': '0', '57': '1177681797', '56': '0', '51': '0', '88': '1', '53': '738eda44bafba017120992a2af649fe4e', '109': '1.000000'}


    ##'99999': '210', NDO_API_FLAPPINGDATA
    ##'48': '1', NDO_DATA_FLAPPINGTYPE
    ##'114': '1234567890as', NDO_DATA_SERVICE
    ##'19': '1177819187', NDO_DATA_COMMENTTIME
    ##'18': '9', 
    ##'3': '0', 
    ##'53': 'localhost', 
    ##'52': '20.00000', NDO_DATA_HIGHTHRESHOLD
    ##'1': '1000', 
    ##'98': '22.76316', NDO_DATA_PERCENTSTATECHANGE
    ##'75': '5.00000', NDO_DATA_LOWTHRESHOLD
    ##'2': '0', 
    ##'4': '1177819187.262553'


    ##'99999': '207', NDO_API_HOSTCHECKDATA
    ##'99997': 79, 
    ##'117': '1177814596.155220',NDO_DATA_STARTTIME
    ##'110': '0', NDO_DATA_RETURNCODE
    ##'118': '0', NDO_DATA_STATE
    ##'25': '1', NDO_DATA_CURRENTCHECKATTEMPT
    ##'42': '4.30391', NDO_DATA_EXECUTIONTIME
    ##'1': '801', 
    ##'3': '0', 
    ##'2': '0', 
    ##'4': '1177814606.188551', 
    ##'99': '', 
    ##'121': '1', NDO_DATA_STATETYPE
    ##'123': '30', 
    ##'71': '0.15400', 
    ##'127': 'check-host-alive', 
    ##'95': 'PING OK - Packet loss = 0%, RTA = 18.91 ms', 
    ##'13': '', 
    ##'12': '0', 
    ##'14': '', 
    ##'76': '3', 
    ##'33': '1177814606.188544', NDO_DATA_ENDTIME
    ##'32': '0', 
    ##'53': '738eda44bafba017120992a2af649fe4e'



    ##'99999': '211', '99997': 3819, 
    ##'60': '0', NDO_DATA_LASTLOGROTATION
    ##'88': '1', NDO_DATA_NOTIFICATIONSENABLED
    ##'80': '0', 
    ##'49': '', 
    ##'47': '1', 
    ##'45': '1', 
    ##'28': '0', 
    ##'1': '1200', '3': '0', '2': '0', '4': '1177685471.173388', '9': '1', '8': '1', 
    ##'96': '1', 
    ##'102': '17733', NDO_DATA_PROCESSID
    ##'103': '0', 
    ##'92': '0', 
    ##'106': '1177681707', NDO_DATA_PROGRAMSTARTTIME
    ##'94': '0', 
    ##'97': '1', 
    ##'78': '0', 
    ##'39': '1', 
    ##'55': '1177685471', 
    ##'50': ''}

    ##'99999': '218', 
    ##'99997': 3820, 
    ##'1': '1500', 
    ##'3': '0', 
    ##'2': '0', 
    ##'4': '1177685477.77915'}



    ##'99999': '213', NDO_API_SERVICESTATUSDATA
    ##'113': '0',
    ##'37': '', 
    ##'98': '0.00000', 
    ##'115': '1', 
    ##'114': 'ssh Server', NDO_DATA_SERVICE
    ##'62': '0', 
    ##'63': '1177681797', NDO_DATA_LASTSTATECHANGE
    ##'64': '0', 
    ##'66': '1177681797', 
    ##'67': '0', 
    ##'83': '1177682097', 
    ##'80': '0', 
    ##'86': '5.000000', 
    ##'84': '0', 
    ##'85': '0', 
    ##'25': '1', 
    ##'26': '0', 
    ##'27': '0', 
    ##'47': '1', 
    ##'45': '1', 
    ##'42': '0.20843', NDO_DATA_EXECUTIONTIME
    ##'1': '1202', 
    ##'3': '0', 
    ##'2': '0', 
    ##'4': '1177681807.192778', 
    ##'7': '0', 
    ##'9': '1', 
    ##'209': '24x7', 
    ##'99': '', 
    ##'76': '3', 
    ##'38': '1', 
    ##'99997': 1718, 
    ##'71': '0.59300', NDO_DATA_LATENCY
    ##'70': '0', 
    ##'103': '1', 
    ##'93': '0', 
    ##'101': '0', 
    ##'95': 'SSH OK - OpenSSH_4.2p1 Debian-7ubuntu3.1 (protocol 2.0)', NDO_DATA_OUTPUT
    ##'97': '1', 
    ##'11': 'check_ssh', NDO_DATA_CHECKCOMMAND
    ##'12': '0', 
    ##'121': '1', 
    ##'61': '1177681797', NDO_DATA_LASTSERVICECHECK
    ##'54': '0', 
    ##'57': '1177681797', NDO_DATA_LASTHARDSTATECHANGE
    ##'56': '0', 
    ##'51': '0', 
    ##'88': '1', 
    ##'53': '738eda44bafba017120992a2af649fe4e', NDO_DATA_HOST
    ##'109': '1.000000'}

    
    ##'99999': '206', NDO_API_SERVICECHECKDATA
    ##'99997': 1719, 
    ##'114': 'ssh Server', NDO_DATA_SERVICE
    ##'117': '1177681797.181939', NDO_DATA_STARTTIME
    ##'110': '0', 
    ##'118': '0', 
    ##'25': '1', 
    ##'42': '0.20843', NDO_DATA_EXECUTIONTIME
    ##'1': '701', 
    ##'3': '0', 
    ##'2': '0', 
    ##'4': '1177681807.192861', 
    ##'99': '', 
    ##'121': '1', 
    ##'123': '60', 
    ##'71': '0.59300', NDO_DATA_LATENCY
    ##'127': '', 
    ##'95': 'SSH OK - OpenSSH_4.2p1 Debian-7ubuntu3.1 (protocol 2.0)', NDO_DATA_OUTPUT
    ##'13': '', 
    ##'12': '0', 
    ##'14': '', 
    ##'76': '3', 
    ##'33': '1177681797.390365', NDO_DATA_ENDTIME
    ##'32': '0', 
    ##'53': '738eda44bafba017120992a2af649fe4e'}NDO_DATA_HOST
    
    
    ##'99999': '206', '99997': 1719, '114': 'ssh Server', '117': '1177681797.181939', '110': '0', '118': '0', '25': '1', '42': '0.20843', '1': '701', '3': '0', '2': '0', '4': '1177681807.192861', '99': '', '121': '1', '123': '60', '71': '0.59300', '127': '', '95': 'SSH OK - OpenSSH_4.2p1 Debian-7ubuntu3.1 (protocol 2.0)', '13': '', '12': '0', '14': '', '76': '3', '33': '1177681797.390365', '32': '0', '53': '738eda44bafba017120992a2af649fe4e'}
    ##'99999': '213', '113': '0', '37': '', '98': '0.00000', '115': '1', '114': 'ssh Server', '62': '0', '63': '1177681797', '64': '0', '66': '1177681797', '67': '0', '83': '1177682097', '80': '0', '86': '5.000000', '84': '0', '85': '0', '25': '1', '26': '0', '27': '0', '47': '1', '45': '1', '42': '0.20843', '1': '1202', '3': '0', '2': '0', '4': '1177681807.192906', '7': '0', '9': '1', '209': '24x7', '99': '', '76': '3', '38': '1', '99997': 1720, '71': '0.59300', '70': '0', '103': '1', '93': '0', '101': '0', '95': 'SSH OK - OpenSSH_4.2p1 Debian-7ubuntu3.1 (protocol 2.0)', '97': '1', '11': 'check_ssh', '12': '0', '121': '1', '61': '1177681797', '54': '0', '57': '1177681797', '56': '0', '51': '1', '88': '1', '53': '738eda44bafba017120992a2af649fe4e', '109': '1.000000'}
    
    ##'99999': '206', 
    ##'117': '0.0',NDO_DATA_STARTTIME
    ##'1': '704',NDO_DATA_TYPE -> 
    ##'123': '0',NDO_DATA_TIMEOUT
    ##'71': '0.01000',NDO_DATA_LATENCY
    ##'14': '',NDO_DATA_COMMANDLINE
    
    ##'99999': '206', 
    ##'117': '1177686642.160895',NDO_DATA_STARTTIME
    ##'1': '700',NDO_DATA_TYPE -> 
    ##'123': '60',NDO_DATA_TIMEOUT
    ##'71': '0.16000',NDO_DATA_LATENCY
    ##'14': '/opt/nagios/libexec/check_http -I 127.0.0.1',NDO_DATA_COMMANDLINE


_pQueue = None
_ndoThread = None


class NdoMain(gocept.runner.appmain):
    """entry point functions for main loops and ndo thread.
    """
    __versRevision = "$LastChangedRevision$"

    def __call__(self, worker_method):
        print "NdoMain.__call__"
        global _pQueue
        global _ndoThread
        main_logger = IkLogger("ndoutils")
        main_logger.log.info("Nagios ndoutils Connector (Rev.: %s)" % \
                             getVersRevision(self.__versRevision) )
        if _pQueue is None:
            main_logger.log.debug("create Queue")
            _pQueue = IkQueue(maxsize=1000)
        if _ndoThread is None:
            _ndoThread = NdoThread(_pQueue)
            _ndoThread.setDaemon(True)
            _ndoThread.start()
        return gocept.runner.appmain.__call__(self, worker_method)


@NdoMain(ticks=1.0, principal='zope.mgr')
def runner():
    """ this function will run every second
    """
    # import in this context
    global _pQueue
    import zope.app.component.hooks
    import zope.security.management
    import zope.app.appsetup.product
    from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor
    site = zope.app.component.hooks.getSite()
    sitemgr = site.getSiteManager()
    admSupervisor = sitemgr.getUtility(IAdmUtilSupervisor, name='AdmUtilSupervisor')
    #print "admSupervisor: ", admSupervisor
    if _pQueue.qsize() > 0:
        print "queue: ", _pQueue.qsize()
    while _pQueue.qsize() > 0:
        tmpObj = _pQueue.get()
        triggerNdoEvent(tmpObj, sitemgr)
        #print "tmpObj: ", tmpObj
