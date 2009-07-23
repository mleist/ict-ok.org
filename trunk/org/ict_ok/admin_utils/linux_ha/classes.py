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
""" cluster, node, ressource classes
buggy
"""

__version__ = "$Id$"

# phython imports


import hb_mini
import locale, gettext
import sys, socket, string, xml, syslog
from xml.dom.minidom import parseString
from pprint import pprint

sys.path.append("/usr/share/heartbeat-gui")
sys.path.append("/usr/lib/heartbeat-gui")
from pymgmt import *

debug_level = 0
failed_reason = ""

def debug(string) :
    if debug_level == 0 :
        return
    syslog.syslog(string)
    print string

class RAMeta :
    name = ""
    version = None
    desc = ""
    parameters = []
    actions = []

class Cluster (object):
    """ class for heartbeat cluster
    """
    def __init__(self, ip, user, passwd, id, manager=None):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.__manager = manager
        self.node_options = {}
        self.ressourcen_options = {}
        self.id = id
        
    def getAttributeNameList(self):
        return [u'default-action-timeout', \
u'batch-limit', \
u'start-failure-is-fatal', \
u'stonith-enabled', \
u'symmetric-cluster', \
u'stop-orphan-actions', \
u'stonith-action', \
u'pe-input-series-max', \
u'remove-after-stop', \
u'is-managed-default', \
u'stop-orphan-resources', \
u'no-quorum-policy', \
u'default-resource-failure-stickiness', \
u'pe-warn-series-max', \
u'pe-error-series-max', \
u'cluster-delay', \
u'default-resource-stickiness', \
u'startup-fencing' \
u'cluster_recheck_interval', \
u'election_timeout', \
u'crmd-integration-timeout', \
u'shutdown_escalation', \
u'crmd-finalization-timeout', \
u'dc_deadtime' \
u'node', \
u'cluster', \
u'deadtime', \
u'warntime', \
u'watchdog', \
u'apiauth', \
u'logfacility', \
u'keepalive', \
u'nice_failback', \
u'auto_failback', \
u'have_quorum', \
u'hopfudge', \
u'msgfmt', \
u'hbversion', \
u'baud', \
u'udpport', \
u'debugfile', \
u'normalpoll', \
u'logfile', \
u'initdead', \
u'stonith', \
u'debug', \
u'deadping']
   
    def getAttributeByName(self, attr):
        """ get one of the following attributes
        [u'default-action-timeout',
        u'batch-limit',
        u'start-failure-is-fatal',
        u'stonith-enabled',
        u'symmetric-cluster',
        u'stop-orphan-actions',
        u'stonith-action',
        u'pe-input-series-max',
        u'remove-after-stop',
        u'is-managed-default',
        u'stop-orphan-resources',
        u'no-quorum-policy',
        u'default-resource-failure-stickiness',
        u'pe-warn-series-max',
        u'pe-error-series-max',
        u'cluster-delay',
        u'default-resource-stickiness',
        u'startup-fencing']
        [u'cluster_recheck_interval',
        u'election_timeout',
        u'crmd-integration-timeout',
        u'shutdown_escalation',
        u'crmd-finalization-timeout',
        u'dc_deadtime']
        [u'node',
         u'cluster',
         u'deadtime',
         u'warntime',
         u'watchdog',
         u'apiauth',
         u'logfacility',
         u'keepalive',
         u'nice_failback',
         u'auto_failback',
         u'have_quorum',
         u'hopfudge',
         u'msgfmt',
         u'hbversion',
         u'baud',
         u'udpport',
         u'debugfile',
         u'normalpoll',
         u'logfile',
         u'initdead',
         u'stonith',
         u'debug',
         u'deadping']
        """
        unicode(attr)
        meta_pengine = self.__get_crm_metadata("pengine")
        meta_crmd = self.__get_crm_metadata("crmd")
        pengine_list = self.__get_crm_config(meta_pengine)
        crmd_list = self.__get_crm_config(meta_crmd)
        #pprint(pengine_list.keys())
        #pprint(crmd_list.keys())
        #pprint(self.__get_cluster_config().keys())
        if(pengine_list.has_key(attr)):
            return pengine_list[attr]
        elif(crmd_list.has_key(attr)):
            return crmd_list[attr]
        elif(self.__get_cluster_config().has_key(attr)):
            return self.__get_cluster_config()[attr]
        else:
            return None

    def __get_cluster_config(self) :
        hb_attr_names = [u"apiauth",u"auto_failback",u"baud",u"debug",u"debugfile",
                         u"deadping",u"deadtime",u"hbversion",u"hopfudge",
                         u"initdead",u"keepalive",u"logfacility",u"logfile",
                         u"msgfmt",u"nice_failback",u"node",u"normalpoll",
                         u"stonith",u"udpport",u"warntime",u"watchdog", u"cluster"]
        values = self.__manager.query("hb_config")
        if values == None :
            return None
        config = dict(zip(hb_attr_names,values))
        value = self.__manager.query("crm_config\nhave_quorum")
        if value != None and value != []:
            config[u"have_quorum"] = value[0]
        return config

    def __get_crm_metadata(self, crm_cmd) :
        if crm_cmd == None :
            return None
        lines = self.__manager.query("crm_metadata\n%s"%(crm_cmd),True)
        if lines == None :
            return None
        meta_data = ""
        for line in lines :
            if len(line)!= 0 :
                meta_data = meta_data + line + "\n"
        try :
            doc_xml = parseString(meta_data).documentElement
        except xml.parsers.expat.ExpatError:
            debug("fail to parse the metadata of ")
            return None
        meta = RAMeta()
        meta.name = doc_xml.getAttribute("name")
        meta.version = ""
        version_xml = doc_xml.getElementsByTagName("version")
        if version_xml != [] and version_xml[0] in doc_xml.childNodes :
            meta.version = version_xml[0].childNodes[0].data
        meta.longdesc = self.__manager.get_locale_desc(doc_xml, "longdesc");
        meta.shortdesc = self.__manager.get_locale_desc(doc_xml, "shortdesc");
        meta.parameters = []
        for param_xml in doc_xml.getElementsByTagName("parameter") :
            param = {}
            param["name"] = param_xml.getAttribute("name")
            param["unique"] = param_xml.getAttribute("unique")
            param["longdesc"] = self.__manager.get_locale_desc(param_xml, "longdesc");
            param["shortdesc"] = self.__manager.get_locale_desc(param_xml, "shortdesc");
            content_xml = param_xml.getElementsByTagName("content")[0]
            content = {}
            content["type"] = content_xml.getAttribute("type")
            content["default"] = content_xml.getAttribute("default")
            if content["type"] == "enum":
                values_tag = "Allowed values:"
                index = param["longdesc"].rfind(values_tag)
                if index != -1:
                    strings = param["longdesc"][index+len(values_tag):].split(",")
                    content["values"] = []
                    for string in strings:
                        content["values"].append(string.strip())
            param["content"] = content
            meta.parameters.append(param)
        return meta

    def __get_all_rsc_id(self) :
        return self.__manager.query("all_rsc")

    def __get_crm_config(self, metadata):
        config = {}
        for parameter in metadata.parameters:
            value = self.__manager.query("crm_config\n%s"% \
                                  str(parameter["name"]))
            if value == None or value == []:
                continue
            if value == [""]:
                config[parameter["name"]] = str(parameter["content"]["default"])
            else:
                config[parameter["name"]] = value[0]
        return config

    def __update_crm_config(self, metadata, new_crm_config) :
        for k,v in new_crm_config.iteritems() :
            value = self.__manager.query("crm_config\n"+str(k))
            if value == [""]:
                for parameter in metadata.parameters:
                    if parameter["name"] == k:
                        cur_value = str(parameter["content"]["default"])
            else:
                cur_value = value[0]
            if cur_value != v :
                self.__manager.do_cmd("up_crm_config\n"+str(k)+"\n"+v)
                if failed_reason != "" :
                    print failed_reason

    def __get_all_nodes(self) :
        """ return a list of strings with node-names
        """
        all_nodes = self.__manager.query("all_nodes")
        return all_nodes
    
    def getNodes(self):
        """ return a list of node objects
        """
        retList = []
        nodenames = self.__get_all_nodes()
        for nodename in nodenames:
            retList.append(Node(nodename, self.__manager))
        return retList

    def __get_active_nodes(self):
        active_nodes = self.__manager.query("active_nodes")
        return active_nodes
    
    def getActiveNodes(self):
        """ return a list of active node objects
        """
        self.__manager.cache_clear()
        retList = []
        nodenames = self.__get_active_nodes()
        for nodename in nodenames:
            retList.append(Node(nodename, self.__manager))
        return retList

    def __get_crm_nodes(self):
        return self.__manager.query("crm_nodes")

    def get_children(self):
        """ return a list of node objects
        """
        retList = []
        nodenames = self.__get_crm_nodes()
        for nodename in nodenames:
            retList.append(Node(nodename, self.__manager))
        return retList
    
    def __get_all_rsc_id(self) :
        return self.__manager.query("all_rsc")

    def __get_rsc_sub_rsc(self, rsc_id) :
        sub_rscs = self.__manager.query("sub_rsc\n"+rsc_id)
        if sub_rscs != None :
            for sub_rsc in sub_rscs :
                self.__manager.parent[sub_rsc] = rsc_id
        return sub_rscs

    def getRessources(self):
        """ returns a list of Rsc running in cluster NO HIERARCHY
        """
        retList = []
        rscnames = self.__get_all_rsc_id()
        for rscname in rscnames:
            rscsubnames = self.__get_rsc_sub_rsc(rscname)
            retList.append(Ressource(rscname, self.__manager))
            for rscsubname in rscsubnames:
                retList.append(Ressource(rscsubname, self.__manager))
        return retList

    def __add_group(self, group) :
        if len(group["id"]) == 0 :
            print("the ID can't be empty")
            return
        if self.__rsc_exists(group["id"]):
            print("the ID already exists")
            return
        cmd = "add_grp\n"+group["id"]
        for param in group["params"] :
            cmd += "\n"+param["id"]
            cmd += "\n"+param["name"]
            cmd += "\n"+param["value"]
        self.__manager.do_cmd(cmd)
        if failed_reason != "" :
            print(failed_reason)

    def __add_native(self, rsc) :
        if self.__rsc_exists(rsc["id"]) :
            print("the ID already exists")
            return
        cmd = "add_rsc"
        cmd += "\n"+rsc["id"]
        cmd += "\n"+rsc["class"]
        cmd += "\n"+rsc["type"]
        cmd += "\n"+rsc["provider"]
        cmd += "\n"+rsc["group"]
        cmd += "\n"+rsc["advance"]
        cmd += "\n"+rsc["advance_id"]
        cmd += "\n"+rsc["clone_max"]
        cmd += "\n"+rsc["clone_node_max"]
        cmd += "\n"+rsc["master_max"]
        cmd += "\n"+rsc["master_node_max"]
        cmd += "\n"+rsc["new_group"]
        for param in rsc["params"] :
            cmd += "\n"+param["id"]
            cmd += "\n"+param["name"]
            cmd += "\n"+param["value"]
        self.__manager.do_cmd(cmd)
        if failed_reason != "" :
            print(failed_reason)
        group_id = rsc["group"]
        if group_id != None and group_id != "" :
            ordered = self.__manager.cache_lookup(group_id+"\nordered")
            if ordered != None :
                new_metaattrs = [{"id": group_id + "_metaattr_ordered" ,
                                  "name": "ordered", "value": ordered}]
                self.__manager.update_attrs("up_rsc_metaattrs\n"+group_id,"del_rsc_metaattr",
                                     [], new_metaattrs, ["id","name","value"]);
                self.__manager.cache_delkey(group_id+"\nordered")
            collocated = self.__manager.cache_lookup(group_id+"\ncollocated")
            if collocated != None :
                new_metaattrs = [{"id": group_id + "_metaattr_collocated" ,
                                  "name": "collocated", "value": collocated}]
                self.__manager.update_attrs("up_rsc_metaattrs\n"+group_id,"del_rsc_metaattr",
                                     [], new_metaattrs, ["id","name","value"]);
                self.__manager.cache_delkey(group_id+"\ncollocated")

    def __rsc_exists(self, rsc_id) :
        return rsc_id in self.__get_all_rsc_id()

    def update_rsc_attr(self, rid, name, value) :
        self.__manager.do_cmd("up_rsc_attr\n%s\n%s\n%s"%(rid,name,value))

    def get_dc(self):
        """ gives the designated coordinator
        """
        dc_node = Node(self.__manager.query("dc"), self.__manager)
        return dc_node # designated coordinator
    
    def get_constraints(self, type):
        """ returns a list of constraint-ids
        """
        id_list = self.__manager.query("get_cos\n"+type)
        constraints = []
        for id in id_list :
            constraints.append(self.__get_constraint(type, id))
        return constraints

    def __get_constraint(self, type, id) :
        if type == "rsc_location" :
            location_attr_names = ["id","rsc","score", "boolean_op"]
            expr_attr_names = ["id","attribute","operation","value"]
            attrs = self.__manager.query("get_co\nrsc_location\n"+id)
            if attrs == None :
                return None
            location = dict(zip(location_attr_names,attrs[:4]))
            location["exprs"] = []
            for i in range((len(attrs)-len(location_attr_names))/len(expr_attr_names)) :
                expr = dict(zip(expr_attr_names,attrs[4+i*4:8+i*4]))
                location["exprs"].append(expr)
            return location
        elif type == "rsc_order" :
            order_attr_names = ["id","from","type","to"]
            attrs = self.__manager.query("get_co\nrsc_order\n" + id)
            if attrs == None :
                return None
            order = dict(zip(order_attr_names,attrs))
            return order
        elif type == "rsc_colocation" :
            colocation_attr_names = ["id","from","to","score"]
            attrs = self.__manager.query("get_co\nrsc_colocation\n" + id)
            if attrs == None :
                return None
            colocation = dict(zip(colocation_attr_names,attrs))
            return colocation
    
    def update_constraint(self, type, constraint) :
        """ update a constraint with type ("rsc_location", "rsc_order",
        "rsc_colocation") and constraint dict (example in migration code)
        """
        if constraint["id"] in self.get_constraints(type) :
            self.__manager.do_cmd("del_co\n"+type+"\n" + constraint["id"])
        if type == "rsc_location" :
            self.__manager.do_cmd("del_co\nrsc_location\n"+constraint["id"])
            cmd = "up_co\nrsc_location\n%s\n%s\n%s\n%s"% \
                (constraint["id"],constraint["rsc"],constraint["score"],constraint["boolean_op"])
            for expr in constraint["exprs"] :
                cmd = cmd + "\n" + expr["id"] + "\n" + expr["attribute"] + \
                    "\n" + expr["operation"] + "\n" + expr["value"]
        elif type == "rsc_order" :
            cmd = "up_co\nrsc_order\n%s\n%s\n%s\n%s"% \
                (constraint["id"],constraint["from"],constraint["type"],constraint["to"])
        elif type == "rsc_colocation" :
            cmd = "up_co\nrsc_colocation\n%s\n%s\n%s\n%s"% 	(constraint["id"],constraint["from"],constraint["to"],constraint["score"])
        self.__manager.do_cmd(cmd)
    
    def unmigrate(self, ressource):
        """ unmigrate our migration by ressource
        ressource: object type
        retruns nothing
        """
        constraint_id = "ict-migrate-%s" % ressource.name
        self.__manager.do_cmd("del_co\nrsc_location\n" + constraint_id)

        
    def migrate(self, ressource, destinationnode=None):
        """ migrate by ressource (object) optional with destination Node (object)
        returns nothing
        """
        if(destinationnode != None):
            checklist = []
            for node in self.getNodes():
                checklist.append(node.name)
            if(destinationnode.name in checklist):
                dict = {'boolean_op': '',
                        'exprs': [{'attribute': '#uname', 'id': 'cli-prefer-expr-%s' % ressource.name,
                                   'operation': 'eq','attribute': "#uname", 'type': 'string',
                                   'value': destinationnode.name}], 
                        'id': 'ict-migrate-%s' % ressource.name, 
                        'rsc': ressource.name, 
                        'score': 'INFINITY'}
            else:
                failed_reason = "Destination node not found (Cluster.migrate())"
        if(destinationnode == None):
            dict = {'boolean_op': '',
                    'exprs': [{'attribute': '#uname', 'id': 'cli-standby-expr-%s' % ressource.name,
                               'operation': 'eq','attribute': "#uname", 'type': 'string',
                               'value': ressource.get_rsc_running_on().name}], 
                    'id': 'ict-migrate-%s' % ressource.name, 
                    'rsc': ressource.name, 
                    'score': '-INFINITY'}
        self.update_constraint("rsc_location", dict)


class Node (object):
    """ class for heartbeat node
    """
    def __init__(self, name, manager=None):
        self.__manager = manager
        self.name = name
        
    def __str__(self):
        return u"Node[%s]" % (self.name)

    def get_nodetype(self):
        """returns node type (string)
        """
        return self.__manager.query("node_type\n%s" % self.name)
    
    def getAttributeNameList(self):
        """return a list of attributes that u can use with getAttributeByNam
        """
        return ["uname", "online","standby", "unclean", "shutdown",
                           "expected_up","is_dc","type"]
    
    def getAttributeByName(self, attr):
        """ returns a Attribute or false by expecting an attrbiutename (string)
        """
        list = self.__get_node_config()
        if(list.has_key(attr)):
            return list[attr]
        else:
            return False
    
    def __get_node_config(self) :
        node_attr_names = ["uname", "online","standby", "unclean", "shutdown",
                           "expected_up","is_dc","type"]
        values = self.__manager.query("node_config\n%s" % self.name)
        if values == None :
            return None
        config = dict(zip(node_attr_names,values))
        return config
# get running rsc
    
    def __get_running_rsc(self):
        return self.__manager.query("running_rsc\n%s" % self.name)


class Ressource(object):
    """ class for heartbeat ressource
    """
    def __init__(self, name, manager=None, parent=None):
        self.name = name
        self.__manager = manager
        self.parent = parent

    def get_rsc_type(self) :
        """returns ressource type (string)
        """
        return self.__manager.query("rsc_type\n"+self.name)[0]

    def get_rsc_status(self) :
        """returns ressource status (string)
        """
        return self.__manager.query("rsc_status\n"+self.name)[0]

    def get_rsc_running_on(self):
        """ returns node (object) where the rsc is running
        """
        #self.__manager.query("rsc_running_on\n"+self.name) returns List but we think a rsc is exclusive
        node = Node(self.__manager.query("rsc_running_on\n"+self.name)[0], self.__manager)
        return node

    def getchildren(self):
        """ returns a list of ressources (ocject) that are in rsc
        """
        retList = []
        sub_rscs = self.__manager.query("sub_rsc\n"+self.name)
        if sub_rscs != None :
            for sub_rsc in sub_rscs :
                retList.append(Ressource(sub_rsc, self.__manager, self))
        return retList

    def getAttributeNameList(self):
        """return a list of attributes that u can use with getAttributeByNam
        """
        retList = []
        rsc_attr_names = ["id", "description", "class", "provider", 
                          "type", "is_managed","restart_type",
                          "multiple_active","resource_stickiness",
                          "resource_failure_stickiness"]
        op_attr_names = ["id", "name","description","interval","timeout",
                         "start_delay","disabled","role","prereq","on_fail"]
        param_attr_names = ["id", "name", "value"]
        meta_attr_names = ["id", "name", "value"]
        retList.extend(rsc_attr_names)
        retList.extend(op_attr_names)
        retList.extend(param_attr_names)
        return retList
    
    def getAttributeByName(self, attr):
        """ gets one of the following Attributes:
        ['id',
        'description',
        'class',
        'provider',
        'type',
        'is_managed',
        'restart_type',
        'multiple_active',
        'resource_stickiness',
        'resource_failure_stickiness']
       ['id',
        'name',
        'description',
        'interval',
        'timeout',
        'start_delay',
        'disabled',
        'role',
        'prereq',
        'on_fail']
       ['id', 'name', 'value']
       ['id', 'name', 'value']
        """
        (attrs, running_on, metaattrs, params, ops) = self.__get_rsc_info()
        #print "----------pprint(attrs)------------"
        #pprint(attrs)
        #print "----------pprint(metaattrs)-------------"
        #pprint(metaattrs)
        #print "------------pprint(params)-----------"
        #pprint(params)
        #print "------------print(ops)-----------"
        #pprint(ops)
        if(attrs.has_key(attr)):
            return attrs[attr]
        #elif(params.has_key(attr)):
            #return params[attr]
        #elif(ops.has_key(attr)):
            #return ops.has_key[attr]
        else:
            return False
        
    def getMetaAtributesByName(self, attr):
        """ returns meta-attribute Value by expecting attribute name
        """
        (attrs, running_on, metaattrs, params, ops) = self.__get_rsc_info()
        retList = []
        for element in metaattrs:
            if(element.has_key(attr)):
                retList.append(element[attr])
        return retList
    
    def getDictMetaAtributesByName(self, attr, value):
        """ returns meta-attribute dict by expecting attribute name
        """
        (attrs, running_on, metaattrs, params, ops) = self.__get_rsc_info()
        for element in metaattrs:
            if(element.has_key(attr)):
                if(element[attr] == value):
                    return element
        return None

    def getMetaAtributes(self, attr):
        """ returns all meta-attributes
        """
        (attrs, running_on, metaattrs, params, ops) = self.__get_rsc_info()
        return metaattrs
    
    def __get_rsc_info(self) :
        """ return a tuple of:
        (attrs, running_on, metaattrs, params, ops)
        """
        rsc_attr_names = ["id", "description", "class", "provider", 
                          "type", "is_managed","restart_type",
                          "multiple_active","resource_stickiness",
                          "resource_failure_stickiness"]
        op_attr_names = ["id", "name","description","interval","timeout",
                         "start_delay","disabled","role","prereq","on_fail"]
        param_attr_names = ["id", "name", "value"]
        meta_attr_names = ["id", "name", "value"]
        #pprint(rsc_attr_names)
        #pprint(op_attr_names)
        #pprint(param_attr_names)
        #pprint(meta_attr_names)
        attr_list = self.__manager.query("rsc_attrs\n%s"%self.name)
        attrs = {}
        if attr_list != None :
            attrs = dict(zip(rsc_attr_names, attr_list))
        running_on = self.__manager.query("rsc_running_on\n%s"%self.name)
        raw_metaattrs = self.__manager.query("rsc_metaattrs\n%s"%self.name)
        metaattrs = self.__manager.split_attr_list(raw_metaattrs, meta_attr_names)
        raw_params = self.__manager.query("rsc_params\n%s"%self.name)
        params = self.__manager.split_attr_list(raw_params, param_attr_names)
        raw_ops = self.__manager.query("rsc_full_ops\n%s"%self.name)
        raw_ops = raw_ops[1:]
        ops = self.__manager.split_attr_list(raw_ops, op_attr_names)
        return (attrs, running_on, metaattrs, params, ops)