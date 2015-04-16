#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
import string
"""

"""

lower = re.compile(r'^([a-z]|_|-|[A-Z]|[0-9])*$')
lower_colon = re.compile(r'^([a-z]|_|-|[A-Z]|[0-9])*(:([a-z]|_|-|[A-Z]|[0-9])*)+$')
problemchars = re.compile(r'^([a-z]|_|-|[A-Z]|[0-9])*[\?\.\$\^!@#%\*]+([a-z]|_|-|[A-Z]|[0-9])*$')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
pp = pprint.PrettyPrinter()
mapping = {"St": "Street",
           "St.": "Street",
           "Ave": "Avenue",
           "Rd": "Road",
           "Rd.": "Road",
           "Blvd": "Boulevard"
           }


def update_s_name(value):
    words = value.split(" ")
    new_s_type = mapping.get(words[-1], None)
    if new_s_type is not None:
        words[-1] = new_s_type
    return " ".join(words)


def transform_value(key, value):
    if key == "addr:street":
        value = update_s_name(value)
    return value



def add_tags(element, node):
    for tag in element.findall('tag'):
        key = string.replace(tag.attrib['k'].lower(), "-", "_")
        value = tag.attrib['v']
        value = transform_value(key, value)
        if lower.match(key):
            node[key] = value
        elif problemchars.match(key):
            pass
        elif lower_colon.match(key):
            split_key = key.split(':')
            node_i = node
            for key in split_key[0:-1]:
                if node_i.get(key, None) is None or type(node_i[key]) is not dict:
                    node_i[key] = {}
                    node_i = node_i[key]
                else:
                    node_i = node_i[key]
            node_i[split_key[-1]] = value


def add_attributes(element, node):
    node['created'] = {}
    for key in element.attrib.keys():
        if key in CREATED:
            node['created'][key] = element.attrib[key]
        elif not (key == 'lat' or key == 'lon'):
            node[key] = element.attrib[key]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" or element.tag == "relation":
        add_attributes(element, node)
        if element.tag=='node':
            node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]
            node['elem_type'] = 'node'
        elif element.tag == "way":
            node['elem_type'] = 'way'
            node['node_refs'] = []
            for nd in element.findall('nd'):
                node['node_refs'].append(nd.attrib['ref'])
        elif element.tag == "relation":
            node["elem_type"] = "relation"
            node["members"] = []
            for mem in element.findall('member'):
                node["members"].append(mem.attrib['ref'])
        add_tags(element, node)
        return node
    else:
        return None


def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == "__main__":
    process_map("../vancouver_canada.osm")