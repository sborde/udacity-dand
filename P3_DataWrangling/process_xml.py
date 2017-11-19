
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from converter import convert_streets, convert_postcodes, convert_housenumber, convert_phonenumber

"""
This script iterate over a given OSM XML file
and converts it to the following format:

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

Phone numbers, post codes, street types and 
house numbers will be cleaned if it is possible.
Else, that attribute will be skipped.
"""

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^(([a-z]|_)*):(([a-z]|_)*)$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def has_position(attributes) :
    return 'lat' in attributes and 'lon' in attributes

def create_position_dict(attributes) :
    """Converts lat & lon value to number and returns in a list"""
    
    latitude = float(attributes['lat'])
    longitude = float(attributes['lon'])
    
    return [latitude, longitude]

def create_creation_dict(attributes) :
    """Creates a dictionary for creation attributes"""
    
    creation_dict = {}
    creation_dict['version'] = attributes['version']
    creation_dict['changeset'] = attributes['changeset']
    creation_dict['timestamp'] = attributes['timestamp']
    creation_dict['user'] = attributes['user']
    creation_dict['uid'] = attributes['uid']
    
    return creation_dict

def shape_element(element):
    node = {}
    
    tag_type = element.tag
    if re.match(re.compile(r'^(node|way)$'), tag_type) :
        
        attributes = element.attrib
        
        node['id'] = attributes['id']
        node['type'] = tag_type
        
        if 'visible' in attributes: 
            node['visible'] = attributes['visible']
        
        if has_position(attributes) :
            node['pos'] = create_position_dict(attributes)
        
        node['created'] = create_creation_dict(attributes)
        
        for tag in element.iter('tag') :
            
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
                            if addr_dict is None :
                                continue
                        else :
                            addr_dict = {}
                            
                        address_part_name = m.group(3)
                        
                        if address_part_name == 'street' :
                            clean_value = convert_streets.convert_street(attribs['v'])    
                        elif address_part_name == 'postcode' :
                            clean_value = convert_postcodes.convert_postcodes(attribs['v'])
                        elif address_part_name == 'housenumber' : 
                            clean_value = convert_housenumber.convert_housenumber(attribs['v'])
                        else :
                            clean_value = attribs['v']

                        if clean_value is None :
                            node['address'] = None
                        else :
                            addr_dict[address_part_name] = clean_value
                            node['address'] = addr_dict
                            

                           
                    else :                   
                        node[m.group(1).replace(':', '_')] = m.group(3)
                        
                elif thisK == 'phone' :
                    clean_value = convert_phonenumber.convert_phone(attribs['v'])
                    
                    if clean_value['clean'] :
                       node['phone'] = clean_value['clean']

                else :
                    node[thisK] = attribs['v']
                    
        if element.tag == 'way' :
            node_refs = []
            for ndref in element.iter("nd") :
                node_refs.append(ndref.attrib['ref'])
            node['node_refs'] = node_refs
        
        if 'name' in node and node['name'] == 'ru' :
            return node
        else :
            return None
    else:
        return None

def debug_process(file_in) :
    for _, element in ET.iterparse(file_in):
        el = shape_element(element)
        if el:            
            print(json.dumps(el, indent=2))

def process_map(file_in, pretty = False):
    
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
    #process_map('ds/budapest.osm')
    debug_process('ds/budapest.osm')