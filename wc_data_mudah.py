# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:35:42 2018

@author: Aziz
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import csv
import numpy as np
import os.path
import datetime


url = 'https://www.mudah.my/'




#select url
r1 = url

# define file name
fname = 'sell_data.csv'

r = requests.get(r1)
next_page = []
soup = BeautifulSoup(r.content, "html.parser")
page = soup.findAll("div",{"class": "listing_thumbs_resultcontainer"})

#next page url
page1 = str(page)
page1 = page1.replace("&amp;", "&") #edit format url page
page2= page1.split("\"")
pagez = [elem1 for elem1 in page2 if elem1.startswith("https")]
pagez = pagez[:-2] #the last two is repeated url.


if(len(pagez)>0):
    pagez.insert(0,r1)
    next_page = pagez
    last = len(next_page)
else:
    next_page = (r1)
    last = 1

for pg in range(0,last):
    #print (pg)
    if(len(pagez)==0):
        r = requests.get(next_page)
    else:
        r = requests.get(next_page[pg])
    #print (r)
       
    data_scrap = []
    title_only = []
    price_only =[]
    date_only=[]
    area_only=[]
    category=[]
 
    soup = BeautifulSoup(r.content, "html.parser")
        
    title = soup.findAll("h2",{"class": "list_title"})
    price1 = soup.findAll("div", {"class": "ads_price"})
    date_location = soup.findAll("div",{"class": "location bottom_info"})
    category = soup.findAll("div",{"class": "display-block"},{"title":"Category"})
    

    for i in range(len(title)-1):
        #item
        select_title = str(title[i]) 
        stringafterword = re.split('\\btitle\\b',select_title)[-1] #\b = Matches the empty string, but only at the beginning or end of a word
        crop_title = stringafterword[2:]
        final_title = crop_title.split("\">")[0] # throw all this and after '">' symbol,backslash (\) is to allowed this quote character " in searching procedure 
    
            
        #price
        price_temp = price1[i].text
        price = int(''.join(filter(str.isdigit, price_temp)))
        price = str(price)
        
        #date
        select_date = str(date_location[i])
        date_loc_1 = select_date.split("div>")
        date1 = date_loc_1[1][:-10]
            
        if date1==' Today' :
            day1 = datetime.datetime.now().day
            month1 = datetime.datetime.now().strftime("%b") #format of strftime - month
    
            s = "-"
            seq = (str(day1), month1) # This is sequence of strings.
            date_final = s.join( seq )
            
        elif date1==' Yesterday':
            day1 = datetime.datetime.now().day -1
            month1 = datetime.datetime.now().strftime("%b") #format of strftime - month
            s = "-"
            seq = (str(day1), month1) # This is sequence of strings.
            date_final = s.join( seq )
            
        else:
            date_final = date1
    
        #location
        area = date_loc_1[2][19:-2]
    
    
        #append all the result
        title_only.append(final_title)
        price_only.append(price)
        date_only.append(date_final)
        area_only.append(area)
        
    
    #put the list into dataframe
    price_int = pd.to_numeric(price_only) # change price type from string to int
    d = {'date' : date_only, 'area': area_only, 'title': title_only, 'price': price_int} # create dictionary 
    df = pd.DataFrame(d) 
    #reorder the column from '['area', 'date', 'price', 'title']' to 'date, area, title, price'
    cols = df.columns.tolist()
    cols = cols[1:2]+cols[0:1]+cols[-1:]+cols[2:3]
    df = df[cols] # dataframe contains title and price
    #print(df)
    
    #transfer to file
    
    if os.path.isfile(fname):
        df_old = pd.read_csv(fname) # reading from file.
        
        verticalstack=pd.concat([df_old,df],axis=0) # axis 0 is for append below
        verticalstack.to_csv(fname, sep=',', index=False)   
            
    else:
        df.to_csv(fname, sep=',', index=False)
    



