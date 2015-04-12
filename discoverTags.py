#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Discover the variety of tags in the osm data
"""
import xml.etree.ElementTree as ET
import pprint


def count_tags(filename):
        tags = {}
        for event, elem in ET.iterparse(filename):
            tags[elem.tag] = tags.setdefault(elem.tag, 0) + 1
        return tags


if __name__ == "__main__":
    print count_tags("../vancouver_canada.osm")
