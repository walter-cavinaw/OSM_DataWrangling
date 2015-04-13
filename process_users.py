# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Find data on users who have contributed. How often.
"""

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.attrib.get('user', None) is not None:
            users.add(element.attrib['user'])

    return users


if __name__=="__main__":
    users = process_map("../vancouver_canada.osm")
    pprint.pprint(users)