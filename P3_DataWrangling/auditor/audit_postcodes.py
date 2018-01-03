#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for auditing postcode format.

The standard postcode format in Hungary is 
for consecutive digits. Sometimes (especially
in international delivery) they use it with a 
H- prefix to denote the country. Because here
the country is unambigous, I removed if present.
                                   

@author: borde
"""

import sys

sys.path.insert(0, '../')

import xml.etree.cElementTree as ET
import converter.convert_postcodes as convert_postcodes

def audit_postcodes(file_in):
    
    correct_postcodes = 0
    dirty_postcode_set = set()
    
    for _, element in ET.iterparse(file_in):
        if element.tag == 'way' or element.tag == 'node' :
            for tag in element.iter('tag') :            
                if tag.attrib['k'] == 'addr:postcode' :
                    
                    converted = convert_postcodes.convert_postcodes(tag.attrib['v'])
                    
                    
                    if converted is None :
                        dirty_postcode_set.add(tag.attrib['v'])
                    else :
                        correct_postcodes += 1
                    
                       
    
    all_entry = len(dirty_postcode_set) + correct_postcodes
    good_ratio = 100 * correct_postcodes / all_entry
    
    print('The {0:.2f}%% of post codes can be cleaned ({1:d}/{2:d}).'.format(good_ratio, correct_postcodes, all_entry))
    print('{0} post codes cannot be detected. List of invalid entries: '.format(len(dirty_postcode_set)))
    print('; '.join((dirty_postcode_set)))
    
    
if __name__ == '__main__' :
    audit_postcodes('../ds/budapest.osm')