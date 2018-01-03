#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for cleaning postcode format.

The standard postcode format in Hungary is 
for consecutive digits. Sometimes (especially
in international delivery) they use it with a 
H- prefix to denote the country. Because here
the country is unambigous, I removed if present.

@author: borde
"""

import re

postcode_pattern = re.compile(r'^([^\d]*)(\d{4})$')

def convert_postcodes(postcode) :
    
    postcode_m = postcode_pattern.match(postcode)
    
    if not postcode_m :
        return None
    
    postcode = postcode_m.group(2)
    
    return postcode