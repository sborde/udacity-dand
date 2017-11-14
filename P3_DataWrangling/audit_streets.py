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
import re

accepted_street_types = [
        'utca', 'sor', 'fasor', 'tere', 'rakpart',
        'telep', 'liget', 'park', 'Park']

street_tag = re.compile(r'^addr:street$')
street_type_re = re.compile(r'.+\b([A-Za-z]+\.?)$')

def audit_street(file_in):
    street_dict = {}
    for _, element in ET.iterparse(file_in):
        if element.tag == 'way' or element.tag == 'node' :
            for tag in element.iter('tag') :
                k_att = tag.attrib['k']
                v_att = tag.attrib['v']
                
                if street_tag.match(k_att) :
                    m = street_type_re.match(v_att)
                    if m :
                        
                        street_type = m.group(1)
                        if street_type in accepted_street_types : 
                            continue
                        
                        if street_type not in street_dict :
                            street_dict[street_type] = set()
                            
                        street_dict[street_type].add(m.group(0))