#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions for cleaning house numbers.

@author: borde
"""

import re

multi_number_pattern_string = r'\d+(-\d+)?'
slashed_pattern_string = r'(\d+(-\d+)?)\/(([A-Za-z](-[A-Za-z])?)|\d+)?'
letter_pattern_string = r'(\d+(-\d+)?)([A-Za-z])'

housenumber_pattern = {
        'normal': re.compile(r'^' + multi_number_pattern_string + '$'),
        'slashed': re.compile('^'+slashed_pattern_string+'$'),
        'letter': re.compile(r'^' + letter_pattern_string + '$'),
        'multipart_slash': re.compile('^('+slashed_pattern_string +')-('+slashed_pattern_string+')$'),
        'multipart_letter': re.compile('^('+letter_pattern_string +')-('+letter_pattern_string+')$')}

"""
This function checks if any of the given
patterns match with the given house number.
If yes, returns that pattern. Else, return None.
"""
def check_housenumber(house_number) :
    for key, value in housenumber_pattern.items() :
        if value.match(house_number) :
            return key
        
    return None
    
    
"""
Converts the given house number if one of the patterns matches. Else, 
returns None.
"""
def convert_housenumber(house_number) :
    
    
    # Remove space, dash and comma
    house_number = (
            house_number
            .replace(' ', '')
            .replace(',', '')
            .replace(';', '')
            .replace('.', '')
            .upper()
            )
    
    
    match_type = check_housenumber(house_number)
        
    # If only a single number, or number, slash and letter, 
    # it is clean already
    if match_type in ['normal', 'slashed'] :
        return house_number
    
    # If a slash is missing between the number and letter
    if match_type == 'letter' :
        matcher = housenumber_pattern['letter'].match(house_number)
        return matcher.group(1) + '/' + matcher.group(3)
    
    # If a building with multiple numbers was given as 2 independent number
    if match_type == 'multipart_slash' :
        
        matcher = housenumber_pattern['multipart_slash'].match(house_number)
        
        first_number = matcher.group(2)
        first_letter = matcher.group(4)
        second_number = matcher.group(8)
        second_letter = matcher.group(10)
        if first_number == second_number :
            processed = first_number + '/' + first_letter + '-' + second_letter
        elif first_letter == second_letter :
            processed = first_number + '-' + second_number + '/' + first_letter
        else :
            return None
        
        return processed
        
    # If buliding with multiple part was given as 2, without slash
    if match_type == 'multipart_letter' :
        
        matcher = housenumber_pattern['multipart_letter'].match(house_number)
        
        first_number = matcher.group(2)
        first_letter = matcher.group(4)
        second_number = matcher.group(6)
        second_letter = matcher.group(8)
        if first_number == second_number :
            processed = first_number + '/' + first_letter + '-' + second_letter
        elif first_letter == second_letter :
            processed = first_number + '-' + second_number + '/' + first_letter
        else :
            return None
        
        return processed

    