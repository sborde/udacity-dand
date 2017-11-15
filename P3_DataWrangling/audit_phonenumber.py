#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 23:58:36 2017

@author: borde
"""
import xml.etree.cElementTree as ET
import re
import pprint
import convert_phonenumber

valid_phonenum = re.compile(r'^(\+36((([23679]0|1)\d{7})|(([23679][1-9]|[1458][0-9])\d{6})))$')

def audit_phonenumber(file_in) :
    valid_patterns = {'normal': 0}
    nonconform_phone_numbers = set()
    
    for _, element in ET.iterparse(file_in):
        if element.tag == 'way' or element.tag == 'node' :
            for tag in element.iter('tag') :
                k_attr = tag.attrib['k']
                v_attr = tag.attrib['v']
                
                if k_attr == 'phone' : 
                    
                        if matching_pattern :
                            valid_patterns['normal'] += 1
                            
                            
                        if not matching_pattern :
                            nonconform_phone_numbers.add(v_attr)
                        
    pprint.pprint(valid_patterns)
    pprint.pprint(nonconform_phone_numbers)
                
if __name__ == "__main__" :
    audit_phonenumber('ds/budapest_sample.osm')
    