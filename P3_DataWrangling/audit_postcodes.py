#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for auditing street information.

There are some accepted street type defined,
the script collects those values which don't
 comply with them.

@author: borde
"""
import xml.etree.cElementTree as ET
import convert_streets

def audit_street(file_in):
    
    correct_street_number = 0
    dirty_street_set = set()
    for _, element in ET.iterparse(file_in):
        if element.tag == 'way' or element.tag == 'node' :
            for tag in element.iter('tag') :

                
                
                if tag.attrib['k'] == 'addr:postcode' :
                    
                    #converted = convert_streets.convert_street(tag.attrib['v'])
                    
                    print(tag.attrib['v'])
                    
                    """
                    if converted is None :
                        dirty_street_set.add(tag.attrib['v'])
                    else :
                        correct_street_number += 1
                    """
                       
    """
    all_entry = len(dirty_street_set) + correct_street_number
    good_ratio = 100 * correct_street_number / all_entry
    
    print('The {0:.2f}%% of street types can be cleaned ({1:d}/{2:d}).'.format(good_ratio, correct_street_number, all_entry))
    print('{0} street type cannot be detected. List of invalid entries: '.format(len(dirty_street_set)))
    print('; '.join((dirty_street_set)))
    """
if __name__ == '__main__' :
    audit_street('ds/budapest_sample.osm')