# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <s.napiorkowski@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $$
#
""" class for flash mindmapping in freemind (freemind.sourceforge.net)
"""

class MMNode(object):
    """ Builds Freemind-Mindmap
    style dict (all optional)
    {
     #"pos": "right", "left" #buggy
     "node_type": "fork", "bubble"
     "icon": ["BUILTIN_1", "BUILTIN_2", "BUILTIN_3"] // for 3 builtin icons you have to know the names
     "font_i": True // for italic
     "font_b": True // for bold
     "font_name": "SanSerif" // etc.
     "font_size": 10
     "edge_width": 1
     "edge_color": "#000000"
     "cloud_color": "#000000"
     "link": "http://google.de"
    }
    """
    def __init__(self, id, text, style=None, subnodes=None):
        self.text = text
        self.id = id
        self.subnodes = subnodes
        self.style_inner_tag = {}
        self.style_outer_tag = {}
        self.__arrows = []
        self.change_style(style)

    def generate_map(self):
        """ generates File, returns mm_string
        """
        output = '<map version="0.8.1">\n'
        output += self.generate_nodes()
        output += "</map>"
        return output
    
    def generate_nodes(self):
        """ generates Nodes-Xml-String
        """
        style_str = ""
        for key, value in self.style_inner_tag.items():
            style_str += '%s="%s" ' % (key, value)
        xml_string = '<node ID="%s" TEXT="%s" %s>\n' % (self.id, self.text, style_str)
        for key, value in self.style_outer_tag.items():
            xml_string += '<%s ' % key
            for k, v in value.items():
                xml_string += '%s="%s" ' % (k, v)
            xml_string += '/>\n'    
        if len(self.__arrows) > 0:
            for ar in self.__arrows:
                xml_string += ar + "\n"
        if self.subnodes != None:
            if len(self.subnodes) != 0:
                for subnode in self.subnodes:
                    xml_string += subnode.generate_nodes()
        xml_string += '</node>\n'
        return xml_string

    def connect_with_node(self, node, style=None):
        """ conects two Nodes with Arrow
        style dict
        {
          "COLOR": "#e01f1f"
          "ENDARROW": "Default"
          "STARTARROW": "None"
        }
        """
        self.connect_with_node_id(node.id, style)
        
    def connect_with_node_id(self, nodeid, style=None):
        #if not self.style_outer_tag.has_key("arrowlink"):
                #self.style_outer_tag["arrowlink"] = {}
        #else:
            #if self.
        #self.style_outer_tag["arrowlink"]["DESTINATION"] = nodeid
        link = '<arrowlink DESTINATION="%s"' % nodeid
        style_str = ""
        if style != None:
            for key, value in style.items():
                style_str += '%s="%s" ' % (key.upper(), value)
        #for value in self.style_outer_tag.values():
            #if value[:len(link)] == link:
                #value = '%s %s/>' % (link, style_str)
            #else:
        self.__arrows.append('%s %s/>' % (link, style_str))

    def change_style(self, style):
        if style == None:
            self.style_inner_tag = {}
            self.style_outer_tag = {}
            return True
        #if style.has_key("pos"):
            #self.style_inner_tag["POSITION"] = style["pos"]
        if style.has_key("node_type"):
            self.style_inner_tag["STYLE"] = style["node_type"]
        if style.has_key("link"):
            self.style_inner_tag["LINK"] = style["link"]
        if style.has_key("icon"):
            pass
        if style.has_key("font_i"):
            if not self.style_outer_tag.has_key("font"):
                self.style_outer_tag["font"] = {}
            self.style_outer_tag["font"]["ITALIC"] = style["font_i"]
        if style.has_key("font_b"):
            if not self.style_outer_tag.has_key("font"):
                self.style_outer_tag["font"] = {}
            self.style_outer_tag["font"]["BOLD"] = style["font_b"]
        if style.has_key("font_name"):
            if not self.style_outer_tag.has_key("font"):
                self.style_outer_tag["font"] = {}
            self.style_outer_tag["font"]["NAME"] = style["font_name"]
        if style.has_key("font_size"):
            if not self.style_outer_tag.has_key("font"):
                self.style_outer_tag["font"] = {}
            self.style_outer_tag["font"]["SIZE"] = style["font_size"]
        if style.has_key("edge_width"):
            if not self.style_outer_tag.has_key("edge"):
                self.style_outer_tag["edge"] = {}
            self.style_outer_tag["edge"]["WIDTH"] = style["edge_width"]
        if style.has_key("edge_color"):
            if not self.style_outer_tag.has_key("edge"):
                self.style_outer_tag["edge"] = {}
            self.style_outer_tag["edge"]["COLOR"] = style["edge_color"]
        if style.has_key("cloud_color"):
            if not self.style_outer_tag.has_key("cloud"):
                self.style_outer_tag["cloud"] = {}
            self.style_outer_tag["cloud"]["COLOR"] = style["cloud_color"]

    def add_node(self, node):
        if self.subnodes == None:
            self.subnodes = []
        self.subnodes.append(node)
        
    def add_nodes(self, nodes):
        if self.subnodes == None:
            self.subnodes = []
        self.subnodes.extend(nodes)

## Mein erster Node
#node1 = Node("0001", "Hallihallo")
## mein zweiter
#node2 = Node("0002", "node2")
## zur übersichtlichkeit ein style dictionary
#style = {"pos": "right", "font_i": "true", "font_size": 25, "edge_color": "#552255", \
         #"cloud_color": "#ff0000"}
## ein drittes node mit dem style von oben
#node3 = Node("0003", "node3", style)

#nodelist = []
#for i in range(0,10):
    ##node mit id=i, name=node_i und dem style von oben
    #node = Node(i, "node_%s" % i, style)
    ## ich ändere den style des nodes der rest von oben bleibt erhalten:
    #node.change_style({"cloud_color": "#00ff00", "font_size": 12, "pos": "left"})
    #nodelist.append(node)
## an den dritten node händ ich die nodelist
#node3.add_nodes(nodelist)
## and den ersten node den zweiten und dritten
#node1.add_nodes([node2, node3])

##ich generier mir eine map mit node1 in der mitte
#mm_string = node1.generate_map()
##genausogut könnt ich auch sagen
##node3.generate_map(f)