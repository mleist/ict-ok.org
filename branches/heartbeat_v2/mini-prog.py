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
"""superclass for all content-objects
"""

__version__ = "$Id$"

# phython imports
from classes import Cluster, Node, Ressource
import MenuSystem as menusystem
import hb_mini

glbmanager = hb_mini.miniManager()
cluster1 = Cluster("172.16.10.172", "hacluster", "ddd", "172.16.10.172", glbmanager)
if(glbmanager.login(cluster1.ip, cluster1.user, cluster1.passwd) == True):
    print "Connected succesfully"
else:
    print "Connection failure"
    exit()
    

def printNodeNames(data):
    print "\n"
    for node in cluster1.getNodes():
        print "Node: %s" % node.name

def printActiveNodes(data):
    print "\n"
    for node in cluster1.getActiveNodes():
        print "Node: %s" % node.name

def printRessources(data):
    print "\n"
    for rsc in cluster1.getRessources():
        print "Ressource: %s" % rsc.name

def printDC(data):
    print "\n"
    print "Designated Coordniator in Cluster '%s': %s" % (cluster1.ip, cluster1.get_dc().name)

def printAttributeCluster(data):
    print cluster1.getAttributeByName(data)

def printAttributeNode(data):
    print "\n"
    data = eval(data)
    node_name = data[0]
    attr = data[1]
    for node in cluster1.getNodes():
        if(node_name == node.name):
            print node.getAttributeByName(attr)

def printAttributeRsc(data):
    print "\n"
    data = eval(data)
    rsc_name = data[0]
    attr = data[1]
    for rsc in cluster1.getRessources():
        if(rsc_name == rsc.name):
            print rsc.getAttributeByName(attr)

def printChildrenRsc(data):
    print "\n"
    rsc = cluster1.getRessources()[0]
    for sub_rsc in rsc.getchildren():
        print sub_rsc.name

def setRsc(data):
    rsc = cluster1.getRessources()[0]
    rsc_dict = rsc.getDictMetaAtributesByName("name","description")
    print rsc_dict['id']
    print rsc_dict['value']
    print cluster1.update_rsc_attr(rsc_dict['id'], 'value', data)

def mig_z(data):
    for node in cluster1.getNodes():
        if(node.name == "hb166.server.ifdd.de"):
            node1 = node
    rsc = cluster1.getRessources()[9]
    cluster1.migrate(rsc, node1)

def mig(data):
    rsc = cluster1.getRessources()[9]
    cluster1.migrate(rsc)

def umig(data):
    rsc = cluster1.getRessources()[9]
    cluster1.unmigrate(rsc)

def done(data):
    return False

# Sub Menu Attributes; Cluster
list = []
i = 1
for attr in cluster1.getAttributeNameList():
    list.append(menusystem.Choice(i, "Get %s" % attr, attr, None, printAttributeCluster))
    i += 1
list.append(menusystem.Choice(selector=0, value=0, handler=done, description='Return to Main Menu'))
menu_cluster_attr = menusystem.Menu(title = "Attributes", choice_list = list)

# Cluster SubMenu
list = []
list.append(menusystem.Choice(selector=1, handler=printNodeNames, description='Get all Nodes'))
list.append(menusystem.Choice(selector=2, handler=printActiveNodes, description='Get all active Nodes'))
list.append(menusystem.Choice(selector=3, handler=printRessources, description='Get all Ressources'))
list.append(menusystem.Choice(selector=4, handler=printDC, description='Get DC'))
list.append(menusystem.Choice(selector=5, handler=None, description='Get Attribute by Name', subMenu=menu_cluster_attr))
list.append(menusystem.Choice(selector=6, handler=setRsc, value="I have...", description='Set discription1'))
list.append(menusystem.Choice(selector=7, handler=setRsc, value="...a dream.", description='Set discription2'))
list.append(menusystem.Choice(selector=0, value=0, handler=done, description='Return to Main Menu'))
menu_cluster = menusystem.Menu(title = "Cluster Options", choice_list=list)

# SubMenu Attributes; Node
list = []
i = 1
for node in cluster1.getNodes():
    if(node.name == "hb164.server.ifdd.de"):
        node1 = node

for attr in node1.getAttributeNameList():
    list.append(menusystem.Choice(i, "Get %s" % attr,[node1.name, attr], None, printAttributeNode))
    i += 1
list.append(menusystem.Choice(selector=0, value=0, handler=done, description='Return to Main Menu'))
menu_node_attr = menusystem.Menu(title = "Attributes", choice_list = list)

# Node SubMenu
list = []
for node in cluster1.getNodes():
    list.append(menusystem.Choice(selector=1, handler=None, description='Get Attribute by Name from Node %s' % node.name, subMenu=menu_node_attr))
list.append(menusystem.Choice(selector=0, value=0, handler=done, description='Return to Main Menu'))
menu_node = menusystem.Menu("Node Options", list)

# SubMenu Attributes; Rsc
list = []
i = 1
rsc = cluster1.getRessources()[0]
for attr in rsc.getAttributeNameList():
    list.append(menusystem.Choice(i, "Get %s" % attr,[rsc.name, attr], None, printAttributeRsc))
    i += 1
list.append(menusystem.Choice(selector=0, value=0, handler=done, description='Return to Main Menu'))
menu_rsc_attr = menusystem.Menu(title = "Attributes", choice_list = list)

# Rsc SubMenu
list = []
i = 1
for rsc in cluster1.getRessources():
    list.append(menusystem.Choice(i, handler=None, description='Get Attribute by Name from Rsc %s' % rsc.name, subMenu=menu_rsc_attr))
    i+= 1;
list.append(menusystem.Choice(i, "Get children of %s" % rsc.name, None, None, printChildrenRsc))
list.append(menusystem.Choice(selector=0, value=0, handler=done, description='Return to Main Menu'))
menu_rsc = menusystem.Menu("Rsc Options", list)

#Menu
list = []
list.append(menusystem.Choice(selector=1, handler=None, description='Cluster Options', subMenu=menu_cluster))
list.append(menusystem.Choice(selector=2, handler=None, description='Node Options', subMenu=menu_node))
list.append(menusystem.Choice(selector=3, handler=None, description='Rsc Options', subMenu=menu_rsc))
list.append(menusystem.Choice(selector=4, handler=mig, description='Rsc R_IP_173:0 migrieren'))
list.append(menusystem.Choice(selector=5, handler=mig_z, description='Rsc R_IP_173:0 migrieren auf hb166'))
list.append(menusystem.Choice(selector=6, handler=umig, description='Rsc R_IP_173:0 unmigrieren'))
list.append(menusystem.Choice(selector=0, value=0, handler=done, description='Exit'))
menu = menusystem.Menu(title='Information about Cluster: 172.16.10.164', choice_list=list, prompt='What do you want to do? ')

menu.waitForInput()

#cluster1.update_constraint("rsc_location", 
from pprint import pprint
pprint(cluster1.get_constraints("rsc_location"))
pprint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
pprint(cluster1.get_constraint("rsc_location", "Loc_R_IP_172:0"))






 