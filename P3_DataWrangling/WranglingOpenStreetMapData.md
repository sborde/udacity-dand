# Wrangling OpenStreetmapData with MongoDB

**Selected map area:** Budapest, Hungary
(Downloaded from mapzen.com as "Custom extract")

https://www.openstreetmap.org/relation/22719

https://mapzen.com/data/metro-extracts/metro/budapest_hungary/

## Table of contents
<ul style="list-style-type: none;">
    <li><a href="#chap1">1. Problems Encountered in the Map</a></li>
    <li><a href="#chap2">2. Data Overview</a></li>
    <li><a href="#chap3">3. Additional Ideas</a></li>
</ul>

<a id="chap1"></a>
## 1. Problems Encountered in the Map
My first problem was that Hungary doesn't have so many big cities. :) My birth town and the place where I live currently was in the database, but its size was well below the necessary 50MB.

Next, I chose the region where I live (Southern Great Plain in Hungary). It was large enough (around 2GB uncompressed), but this region lays along the border, so there was many foreign street name in it. Finally, I chose Budapest, the capital of Hungary.

After initial audit I found the following potential errors:

 - Invalid streets. I downloaded Budapest, but there were some street which had foreign name.
 - Weird postcodes. Postcodes in Hungary consists of 4 digits. I found four postcodes in different format.
 - Inconsistent house numbers. The basic house number is a single decimal number. If a land was divided, they put a letter after the number like: 17/A, 17/B. But in this dataset this occurred in various forms.

<a id="chap2"></a>
## 2. Data Overview

This section contains basic statistics about the dataset and the MongoDB queries used to gather them.


<a id="chap3"></a>
## 3. Additional Ideas
