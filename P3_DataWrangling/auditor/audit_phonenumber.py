#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function for auditing phone numbers in a file.

@author: borde
"""

import sys

sys.path.insert(0, '../')

import xml.etree.cElementTree as ET
import converter.convert_phonenumber as convert_phonenumber

"""
This function passes a phone number entry to the cleaning function, and 
returns the cleaned and dirty numbers as a tuple.
"""
def audit_single_entry(phone_number_entry) :
    number_dict = convert_phonenumber.convert_phone(phone_number_entry)
    return (number_dict['clean'], number_dict['dirty'])


"""
This function iterate over a given file and 
audits each phonenumber tag. After finishing
with the whole file, statistics will be displayed.
"""
def audit_phonenumbers_in_file(file_in) :
    
    clean_number = 0
    dirty_number_set = set()
    
    for _, element in ET.iterparse(file_in):
        if element.tag == 'way' or element.tag == 'node' :
            for tag in element.iter('tag') :
                if tag.attrib['k'] == 'phone' : 
                    
                    (clean_set, dirty_set) = audit_single_entry(tag.attrib['v'])
                    
                    clean_number += len(clean_set)
                    dirty_number_set = dirty_number_set | set(dirty_set)
                    
    all_phone_entry = clean_number + len(dirty_number_set)
    clean_ratio = 100 * clean_number / all_phone_entry
    
    print('The {0:.2f}%% of phone numbers can be cleaned ({1:d}/{2:d}).'.format(clean_ratio, clean_number, all_phone_entry))
    print('{0} phone number cannot be cleaned. List of invalid entries: '.format(len(dirty_number_set)))
    print(', '.join((dirty_number_set)))
                
if __name__ == "__main__" :
    audit_phonenumbers_in_file('../ds/budapest.osm')
    