#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 00:58:28 2017

@author: borde
"""

import csv

with open('support_CA.csv', 'r') as input_file :
    with open('support_CA_col.csv', 'w') as output_file : 
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        writer.writerow(next(reader))
        for row in reader :
            writer.writerow(row[:-1])