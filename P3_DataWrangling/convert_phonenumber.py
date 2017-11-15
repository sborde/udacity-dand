# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 14:11:06 2017

@author: Sándor
"""

import re

valid_phonenum = re.compile(r'^(\+36((([23679]0|1)\d{7})|(([23679][1-9]|[1458][0-9])\d{6})))$')

def check_phonenum(phone_num) :
    return valid_phonenum.match(phone_num)

def convert_phone(phone_number) :
    
    phone_number_list = {'clean': [], 'dirty': []}
                    
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
        
        
        if check_phonenum(phone_number) :
            phone_number_list['clean'].add(phone_number)
        else :
            phone_number_list['dirty'].add(phone_number)