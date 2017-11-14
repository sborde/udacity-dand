#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 01:41:07 2017

@author: borde
"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
address_prefix = re.compile(r'^addr:(([a-z]|_)*)$')
lower_colon = re.compile(r'^(([a-z]|_)*):(([a-z]|_)*)$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_name = re.compile(r'.+\b([A-Za-z]+\.?)$')






        
def collect_address_element(file_in, element_name) :
    address_part = re.compile(r'^addr:'+element_name+'$')
    
    missing = 0
    counts = {}
    
    for _, element in ET.iterparse(file_in) : 
        if element.tag == 'node' or element.tag == 'way' :
            has_field = False
            for tag in element.iter('tag') :
                if address_part.match(tag.attrib['k']) : 
                    has_field = True
                    this_value = tag.attrib['v']
                    if this_value in counts :
                        counts[this_value] += 1
                    else :
                        counts[this_value] = 1
            if not has_field :
                missing += 1
               
    counts['-'] = missing
    pprint.pprint(counts)
    



def audit():
    file_in = 'ds/budapest_sample.osm'
    #audit_street('ds/budapest.osm', True)
    #audit_housenumber('ds/budapest_sample.osm', True)
    #collect_address_element(file_in, 'street')


if __name__ == "__main__":
    audit()