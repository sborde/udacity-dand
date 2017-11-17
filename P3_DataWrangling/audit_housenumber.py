#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for auditing house numbers.

There is a default format for house numbering but there are 
various ways to write them. This script collects the house numbers
and sort them by type.

@author: borde
"""

import xml.etree.cElementTree as ET
import convert_housenumber


def audit_housenumber(file_in):
    
    clean_housenumber_num = 0
    dirty_housenumbers = set()
    
    for _, element in ET.iterparse(file_in):
        if element.tag == 'way' or element.tag == 'node' :
            for tag in element.iter('tag') :
                if tag.attrib['k'] == 'addr:housenumber' :     
                    result = convert_housenumber.convert_housenumber(tag.attrib['v'])
                    
                    if result is None :
                        dirty_housenumbers.add(tag.attrib['v'])
                    else :
                        clean_housenumber_num += 1
    
    all_housenumber_entry = clean_housenumber_num + len(dirty_housenumbers)
    clean_ratio = 100 * clean_housenumber_num / all_housenumber_entry
    
    print('The {0:.2f}%% of house numbers can be cleaned ({1:d}/{2:d}).'.format(clean_ratio, clean_housenumber_num, all_housenumber_entry))
    print('{0} house number cannot be cleaned. List of invalid entries: '.format(len(dirty_housenumbers)))
    print(', '.join((dirty_housenumbers)))
                    
                
if __name__ == "__main__" :
    audit_housenumber('ds/budapest_sample.osm')