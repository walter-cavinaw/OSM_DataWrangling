"""
Use this to audit the tags for the elements. For example, replacing the "addr:postcode" with "addr:street"
will show all street names that don't end in an expected street type.
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected_street = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Crescent", "Walk", "Highway", "Way", "Mall", "Alley", "Mews", "Broadway"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Ave":"Avenue",
            "Rd":"Road",
            "Rd.":"Road"
            }


def audit_type(types, street_name, expected):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile, type, expected):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag is not None:
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == type:
                    audit_type(street_types, tag.attrib['v'], expected)

    return street_types


def update_name(name, mapping):

    words = name.split(" ")
    words[-1] = mapping.get(words[-1], words[-1])
    name = " ".join(words)

    return name


if __name__ == '__main__':
    street_types = audit("../vancouver_canada.osm", "addr:postcode", expected_street)
    pprint.pprint(street_types.items())
