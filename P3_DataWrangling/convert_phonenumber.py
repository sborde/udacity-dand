# -*- coding: utf-8 -*-
"""
Phone number converter functions.

@author: Sándor
"""

import re

valid_phonenum = re.compile(r'^(\+36((([23679]0|1)\d{7})|(([23679][1-9]|[1458][0-9])\d{6})))$')

def check_phonenum(phone_num) :
    return valid_phonenum.match(phone_num)

"""
This function tries to convert a given phone number to valid format.
If the input contains more phone number separated with ; or , splits
them and process independently. Finally, it collects the numbers in
a dictionary, separately the cleaned numbers and number which cannot
be cleaned.
"""
def convert_phone(phone_number) :
    
    phone_number_dict = {'clean': [], 'dirty': []}
                    
    # If multiple phone numbers were given, split
    if ',' in phone_number :
        phone_number_list = phone_number.split(',')
    elif ';' in phone_number :
        phone_number_list = phone_number.split(';')
    else :
        phone_number_list = [phone_number]
    
    # Iterate over possible phone numbers and clean
    for phone_number in phone_number_list :
        
        # Remove brackets, dashes, slashes, spaces
        phone_number = (
                phone_number
                .replace(' ', '')
                .replace('-','')
                .replace('/','')
                .replace('(','')
                .replace(')','')
            )
        
        # Check old international format
        if phone_number.startswith('0036') : 
            phone_number = '+36' + phone_number[4:]
        
        # Check inland format
        if phone_number.startswith('06') :
            phone_number = '+36' + phone_number[2:]
        
        # Put missing country number
        if (
                (len(phone_number) == 9 or len(phone_number) == 8) and
                check_phonenum('+36'+phone_number)
           ) :
            phone_number = '+36' + phone_number
        
        # Decide if the number is clean or not
        if check_phonenum(phone_number) :
            phone_number_dict['clean'].append(phone_number)
        else :
            phone_number_dict['dirty'].append(phone_number)
            
        return phone_number_dict
            