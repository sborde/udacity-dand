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

accepted_street_types = ['utca', 'sor', 'fasor', 'tere', 'rakpart', 'telep', 'liget', 'park', 'Park']

def audit_street(file_in, pretty = False):
    street_dict = {}
    for _, element in ET.iterparse(file_in):
        if element.tag == 'way' :
            for tag in element.iter("tag") :
                m = address_prefix.match(tag.attrib['k']) 
                if m and m.group(1)=='street' :
                    m2 = street_name.match(tag.attrib['v'])
                    if m2 :
                        if m2.group(1) in accepted_street_types : 
                            continue
                        
                        street_type = m2.group(1)
                        if street_type not in street_dict :
                            street_dict[street_type] = set()
                            
                        street_dict[street_type].add(m2.group(0))
            
    pprint.pprint(street_dict)

def audit_housenumber(file_in, pretty = False):
    weird_housenumber = set()
    weird_postcodes = set()
    nonbp_postcodes = set()
    bp_postcodes = set()
    for _, element in ET.iterparse(file_in):
        if element.tag == 'way' or element.tag == 'node' :
            for tag in element.iter("tag") :
                m = address_prefix.match(tag.attrib['k']) 
                if m and m.group(1)=='housenumber' :
                    m2 = re.match(r'^(\d+)$', tag.attrib['v'])
                    if not m2 :
                        weird_housenumber.add(tag.attrib['v'])
                        
                elif m and m.group(1) == 'postcode' : 
                    m2 = re.match(r'^(\d{4})$', tag.attrib['v'])
                    if not m2 :
                        weird_postcodes.add(tag.attrib['v'])
                    else :
                        if not m2.group(1).startswith('1') :
                            nonbp_postcodes.add(m2.group(1))
                        else :
                            bp_postcodes.add(m2.group(1))
    
    pprint.pprint(weird_housenumber)
    
    pprint.pprint(weird_postcodes)
    
    print('Bp: ' + str(len(bp_postcodes)) + ' Non-BP: ' + str(len(nonbp_postcodes)))
        
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