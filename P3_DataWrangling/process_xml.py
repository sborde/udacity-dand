# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:58:13 2017

@author: Sándor
"""

def count_tags(filename):
    tag_set = {}
    for event, elem in ET.iterparse(filename) :
        if elem.tag in tag_set :
            tag_set[elem.tag] += 1
        else :
            tag_set[elem.tag] = 1
            
    return tag_set