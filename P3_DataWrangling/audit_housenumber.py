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
import re
import pprint

housenumber_tag = re.compile(r'^addr:housenumber$')

slashed_pattern_string = r'(\d+(-\d+)?)\/(([A-Za-z](-[A-Za-z])?|\d+))\.?'
letter_pattern_string = r'\d+(-\d+)?[A-Za-z]'

housenumber_pattern = {
        'normal': re.compile(r'^\d+(-\d+)?\.?$'),
        'slashed': re.compile('^'+slashed_pattern_string+'$'),
        'letter': re.compile(r'^' + letter_pattern_string + '$'),
        'multipart_slash': re.compile('^('+slashed_pattern_string +')-('+slashed_pattern_string+')$'),
        'multipart_letter': re.compile('^('+letter_pattern_string +')-('+letter_pattern_string+')$')}

def audit_housenumber(file_in):
    
    valid_patterns = {'normal': 0, 'slashed': 0, 'letter': 0, 'multipart_slash': 0, 'multipart_letter': 0}
    nonconform_house_numbers = set()
    
    for _, element in ET.iterparse(file_in):
        if element.tag == 'way' or element.tag == 'node' :
            for tag in element.iter('tag') :
                k_attr = tag.attrib['k']
                v_attr = tag.attrib['v']
                
                m = housenumber_tag.match(k_attr)
                
                if m : 
                    matching_pattern = False
                    
                    v_attr = (
                            v_attr
                            .replace(' ', '')
                            .replace(',', '')
                            .replace(';', '')
                            )
                    
                    for key, pattern in housenumber_pattern.items() :
                        matching_pattern = pattern.match(v_attr)
                        if matching_pattern :
                            valid_patterns[key] += 1
                            break
                        
                    if not matching_pattern :
                        nonconform_house_numbers.add(v_attr)
                        
    pprint.pprint(valid_patterns)
    pprint.pprint(nonconform_house_numbers)
                
if __name__ == "__main__" :
    audit_housenumber('ds/budapest_sample.osm')