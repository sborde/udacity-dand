#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 23:58:36 2017

@author: borde
"""
import xml.etree.cElementTree as ET
import re
import pprint

valid_phonenum = re.compile(r'^\+36((([23679]0|1)\d{7})|(([23679][1-9]|[1458][0-9])\d{6}))$')

def audit_phonenumber(file_in) :
    valid_patterns = {'normal': 0}
    nonconform_phone_numbers = set()
    
    for _, element in ET.iterparse(file_in):
        if element.tag == 'way' or element.tag == 'node' :
            for tag in element.iter('tag') :
                k_attr = tag.attrib['k']
                v_attr = tag.attrib['v']
                
                if k_attr == 'phone' : 
                    matching_pattern = False
                    
                    if ',' in v_attr :
                        v_attrl = v_attr.split(',')
                    elif ';' in v_attr :
                        v_attrl = v_attr.split(';')
                    else :
                        v_attrl = [v_attr]
                    
                    for v_attr in v_attrl :
                        v_attr = v_attr.replace(' ', '').replace('-','').replace('/','').replace('(','').replace(')','')
                        
                        if v_attr.startswith('0036') : 
                            v_attr = '+36' + v_attr[4:]
                        if v_attr.startswith('06') :
                            v_attr = '+36' + v_attr[2:]
                        
                        if len(v_attr) == 9 and valid_phonenum.match('+36'+v_attr) :
                            v_attr = '+36' + v_attr
                        
                        if len(v_attr) == 8 and v_attr.startswith('1') and valid_phonenum.match('+36'+v_attr) : 
                            v_attr = '+36' + v_attr
                        
                        matching_pattern = valid_phonenum.match(v_attr)
                        if matching_pattern :
                            valid_patterns['normal'] += 1
                            
                            
                        if not matching_pattern :
                            nonconform_phone_numbers.add(v_attr)
                        
    pprint.pprint(valid_patterns)
    pprint.pprint(nonconform_phone_numbers)
                
if __name__ == "__main__" :
    audit_phonenumber('ds/budapest_sample.osm')
    