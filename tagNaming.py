#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
We need to check here if there are any problematic characters in the key attribute for the tag.
MongoDB does not accept certain characters in field names.
"""


lower = re.compile(r'^([a-z]|_|[1-9])*$')
lower_colon = re.compile(r'^([a-z]|_|[1-9])*(:([a-z]|_|[1-9])*)+$')
problemchars = re.compile(r'^([a-z]|_|[1-9])*[\?\.\$\^!@#%\*]+([a-z]|_|[1-9])*$')


def key_type(element, keys, other):
    if element.tag == "tag":
        key = element.attrib['k']
        if re.match(lower_colon, key):
            keys['lower_colon'] += 1
        elif re.match(problemchars, key):
            keys['problemchars'] += 1
        elif re.match(lower, key):
            keys['lower'] += 1
        else:
            other.add(key)
            keys['other'] += 1

    return keys


def process_map(filename):
    other = set()
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys, other)

    return keys, other


if __name__ == "__main__":
    keys, other_keys = process_map("../vancouver_canada.osm")
    pprint.pprint(keys)
    pprint.pprint(other_keys)