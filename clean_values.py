"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
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
