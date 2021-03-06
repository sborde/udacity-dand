#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for auditing street information.

There are some accepted street type defined,
the script collects those values which don't
 comply with them.

@author: borde
"""

import re

accepted_street_types = [
        'utca', 'sor', 'fasor', 'tere', 'rakpart',
        'telep', 'liget', 'park', 'Park', 'tér',
        'köz', 'út', 'körút', 'sétány', 'útja', 
        'lépcső', 'lejtő', 'árok', 'aluljáró',
        'körtér', 'udvar', 'határsor']

street_abbr_mapping = {'u': 'utca'}

street_type_re = re.compile(r'(.+)\b([A-Za-záéíóöőüűú]+\.?)$')

def convert_street(street) :
    
    street_type = street_type_re.match(street)
    
    if not street_type :
        return None
    
    street_name = street_type.group(1)
    street_type = street_type.group(2)
    
    street_type = (
            street_type
            .lower()
            .replace('.', '')
            )
    
    if street_type in street_abbr_mapping :
        street_type = street_abbr_mapping[street_type]
    
    if street_type in accepted_street_types : 
        return street_name + ' ' + street_type
    
    return None