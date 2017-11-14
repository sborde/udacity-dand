import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB.

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to
update the street names before you save them to JSON.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings.
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^(([a-z]|_)*):(([a-z]|_)*)$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        attributes = element.attrib
        node['id'] = attributes['id']
        node['type'] = element.tag
        
        if 'visible' in attributes: 
            node['visible'] = attributes['visible']
        
        if 'lat' in attributes and 'lon' in attributes :
            node['pos'] = [float(attributes['lat']), float(attributes['lon'])]
            
        creation_dict = {}
        creation_dict['version'] = attributes['version']
        creation_dict['changeset'] = attributes['changeset']
        creation_dict['timestamp'] = attributes['timestamp']
        creation_dict['user'] = attributes['user']
        creation_dict['uid'] = attributes['uid']
        node['created'] = creation_dict
        
        for tag in element.iter("tag") :
            attribs = tag.attrib
            if 'k' in attribs : 
                thisK = attribs['k']
                if problemchars.search(thisK) :
                    continue
                m = lower_colon.search(thisK)
                                
                if m :
                    if m.group(1) == 'addr' :
                        if 'address' in node :
                            addr_dict = node['address']
                        else :
                            addr_dict = {}
                            
                        addr_dict[m.group(3)] = attribs['v']
                        node['address'] = addr_dict
                    else :
                                             
                        node[m.group(1).replace(':', '_')] = m.group(3)
                        
                else :
                    node[thisK] = attribs['v']
                    
        if element.tag == 'way' :
            node_refs = []
            for ndref in element.iter("nd") :
                node_refs.append(ndref.attrib['ref'])
            node['node_refs'] = node_refs


        
        return node
    else:
        return None


def process_map(file_in, pretty = False):
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

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('example.osm', True)
    #pprint.pprint(data)

    correct_first_elem = {
        "id": "261114295",
        "visible": "true",
        "type": "node",
        "pos": [41.9730791, -87.6866303],
        "created": {
            "changeset": "11129782",
            "user": "bbmiller",
            "version": "7",
            "uid": "451048",
            "timestamp": "2012-03-28T18:31:23Z"
        }
    }
    assert data[0] == correct_first_elem
    assert data[-1]["address"] == {
                                    "street": "West Lexington St.",
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369",
                                    "2199822370", "2199822284", "2199822281"]

if __name__ == "__main__":
    test()

#
#def get_user(element):
#    return element.attrib['user']
#
#
#def process_map(filename):
#    users = set()
#    for _, element in ET.iterparse(filename):
#        if 'user' in element.attrib :
#            users.add(get_user(element))
#
#    return users
#
#def count_tags(filename):
#    tag_set = {}
#    for event, elem in ET.iterparse(filename) :
#        if elem.tag in tag_set :
#            tag_set[elem.tag] += 1
#        else :
#            tag_set[elem.tag] = 1
#
#    return tag_set
#
#def key_type(element, keys):
#    if element.tag == "tag":
#        if lower.match(element.attrib['k']) :
#            keys['lower'] += 1
#        elif lower_colon.match(element.attrib['k']) :
#            keys['lower_colon'] += 1
#        elif problemchars.search(element.attrib['k']) :
#            keys['problemchars'] += 1
#        else :
#            keys['other'] += 1
#
#    return keys
#
#def process_map(filename):
#    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
#    for _, element in ET.iterparse(filename):
#        keys = key_type(element, keys)
#
#    return keys
#
#
#street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
#
#
#expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
#            "Trail", "Parkway", "Commons"]
#
## UPDATE THIS VARIABLE
#mapping = { "St": "Street",
#            "St.": "Street"
#            }
#
#
#def audit_street_type(street_types, street_name):
#    m = street_type_re.search(street_name)
#    if m:
#        street_type = m.group()
#        if street_type not in expected:
#            street_types[street_type].add(street_name)
#
#
#def is_street_name(elem):
#    return (elem.attrib['k'] == "addr:street")
#
#
#def audit(osmfile):
#    osm_file = open(osmfile, "r")
#    street_types = defaultdict(set)
#    for event, elem in ET.iterparse(osm_file, events=("start",)):
#
#        if elem.tag == "node" or elem.tag == "way":
#            for tag in elem.iter("tag"):
#                if is_street_name(tag):
#                    audit_street_type(street_types, tag.attrib['v'])
#    osm_file.close()
#    return street_types
#
#def update_name(name, mapping):
#    m = street_type_re.search(name)
#    if m:
#        street_type = m.group()
#        return name.replace(street_type, mapping[street_type])
