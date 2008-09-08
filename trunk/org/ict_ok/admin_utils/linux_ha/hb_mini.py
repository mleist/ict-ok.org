#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2008,
#               Sebastian Napiorkowski
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
""" Small Python Script for heartbeat Communication
buggy
"""

__version__ = "$Id$"

# phython imports

import locale
import sys, socket, string, syslog

#sys.path.append("/usr/share/heartbeat-gui")
#sys.path.append("/usr/lib/heartbeat-gui")
sys.path.append("/opt/ict_ok.org/lib/heartbeat-gui")
from pymgmt import *

debug_level = 0

def debug(string) :
    if debug_level == 0 :
        return
    syslog.syslog(string)
    print string

class miniManager(object):
    """ minimal manager for heartbeat
    """
    connected = False
    server = None
    username = None
    password = None
    cache = {}
    no_update_cache = {}
    parent = {}
    #io_tag = None
    active_nodes = []
    all_nodes = []
    failed_reason = ""
    
    def split_attr_list(self, attrs, keys) :
        attr_list = []
        if attrs != None :
            for i in range(0, len(attrs), len(keys)) :
                attr = {}
                for j in range (0, len(keys)) :
                    attr[keys[j]] = attrs[i+j]
                attr_list.append(attr)
        return attr_list
    
    def login(self, server, username, password):
        """ Connects to hearbeat
        """
        failed_reason = ""
        self.server = server
        ip = ""
        port = ""
        if string.find(server, ":") != -1 :
            server,port = string.split(server,":")
        ip = socket.gethostbyname(server)
        ret = mgmt_connect(ip, username, password, port)
        if ret != 0 :
            if ret == -1 :
                failed_reason = "Can't connect to server"
            elif ret == -2 :
                failed_reason ="Failed in the authentication.\n User Name or Password may be wrong." \
                      "\n or the user doesn't belong to haclient group"
            mgmt_disconnect()
            return False
        self.connected = True
        self.username = username
        self.password = password
        #fd = mgmt_inputfd()
        return True

    def cache_lookup(self, key) :
        if self.cache.has_key(key) :
            return self.cache[key]
        if self.no_update_cache.has_key(key) :
            return self.no_update_cache[key]
        return None
    
    def cache_delkey(self, key) :
        if self.cache.has_key(key) : 
            del self.cache[key]

    def cache_clear(self) :
        self.cache.clear()
    
    def logout(self) :
        mgmt_disconnect()
        #gobject.source_remove(self.io_tag)
        self.connected = False
        

    def query(self, query, keep_in_catch = False) :
        result = self.cache_lookup(query)
        if  result != None :
            return 	result
        result = self.do_cmd(query)
        self.cache_update(query, result, keep_in_catch)
        return result
    
    def do_cmd(self, command) :
        failed_reason = ""
        ret_str = mgmt_sendmsg(command)
        if ret_str == None :
            debug(str(string.split(command, "\n"))+":None")
            failed_reason = "return None"
            return None
        while len(ret_str)>=4 and ret_str[:4] == "evt:" :
            #gobject.idle_add(self.on_event, None, None, ret_str)
            ret_str = mgmt_recvmsg()
            if ret_str == None :
                debug(str(string.split(command, "\n"))+":None")
                failed_reason = "return None"
                return None

        ret_list = string.split(ret_str, "\n")
        if ret_list[0] != "ok" :
            debug(str(string.split(command, "\n"))+":"+ str(ret_list))
            if len(ret_list) > 1 :
                failed_reason = string.join(ret_list[1:],",")
            return None
        debug(str(string.split(command, "\n"))+":"+ str(ret_list))
        return ret_list[1:]
    
    def cache_update(self, key, data, keep_in_cache = False) :
        if not keep_in_cache :
            self.cache[key] = data
        else :
            self.no_update_cache[key] = data

    def get_locale_desc(self, node, tag) :
        desc_en = ""
        desc_match = ""

        (lang, encode) = locale.getlocale()
        if lang == None:
            lang = "en"
        else:
            lang = string.lower(lang)
        if encode == None:	
            encode = ""
        else:	
            encode = string.lower(encode)

        for child in node.childNodes :
            if child.nodeType != node.ELEMENT_NODE :
                continue
            if child.tagName != tag :
                continue
            if len(child.childNodes) == 0:
                break
            langtag = string.lower(child.getAttribute("lang"))
            if langtag == "" :
                desc_en = child.childNodes[0].data
            else :
                langtag = string.split(langtag, ".")
                if string.find(langtag[0], "en") != -1 :
                    desc_en = child.childNodes[0].data
                if len(langtag) == 1 and lang == langtag[0] :
                    desc_match = child.childNodes[0].data
                if len(langtag) == 2 :	
                    if lang == langtag[0] and encode == langtag[1] :
                        desc_match = child.childNodes[0].data	
        if desc_match != "" :
            return desc_match
        return desc_en
    
    def update_attrs(self, up_cmd, del_cmd, old_attrs, new_attrs, keys):
        oldkeys = []
        if old_attrs != None :
            for attr in old_attrs :
                oldkeys.append(attr["id"])

                newkeys = []
        if new_attrs != None :
            for attr in new_attrs :
                newkeys.append(attr["id"])

        for key in oldkeys :
            if key not in newkeys :
                self.do_cmd(del_cmd+"\n"+key)
                if failed_reason != "" :
                    print(failed_reason)

        if new_attrs != [] :		
            for attr in new_attrs:
                cmd = up_cmd
                for key in keys :
                    cmd += "\n" + attr[key]
                self.do_cmd(cmd)
                if failed_reason != "" :
                    print(failed_reason)

#manager = miniManager()

#from pprint import pprint

#if(manager.login("172.16.64.161", "hacluster", "")):
    #print "Connected succesfully"
#else:
    #print "Connection failure"

#pengine_metadata = manager.get_crm_metadata("pengine")
#crmd_metadata = manager.get_crm_metadata("crmd")

##pprint(manager.get_cluster_config()) #HA Informations
#pprint(manager.get_crm_config(pengine_metadata)) #HA Configurations
#pprint(manager.get_crm_config(crmd_metadata)) #HA Advanced
#pprint(manager.get_crm_nodes())




##print "~~~~~~~++++++~~~~~~ get_all_nodes"
###print "-%s-" % str(manager.get_all_nodes())
##mynodes = manager.get_all_nodes()
##pprint(mynodes)
##for mynode in mynodes:
    ##print "~~~~~~~++++++~~~~~~ manager.get_node_config '%s'" % mynode
    ##pprint(manager.get_node_config(mynode))
    ##print "~~~~~~~++++++~~~~~~get_running_rsc '%s'" % mynode
    ##myrscs = manager.get_running_rsc(mynode)
    ##pprint(myrscs)
    ##for myrsc in myrscs:
        ##print "~~~~~~~++++++~~~~~~"
        ##pprint(manager.get_rsc_info(myrsc))

#print "ende"
#manager.logout()

