# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 22:49:50 2019

@author: Harsh R . Solanki
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import csv
from  collections import OrderedDict

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

'''
url = 'https://www.daad.de/deutschland/studienangebote/international-programmes/en/detail/4122/'
print("Opening the file connection...")
uh= urllib.request.urlopen(url, context=ctx)
print("HTTP status",uh.getcode())
html =uh.read().decode()
print(f"Reading done. Total {len(html)} characters read.") 

soup = BeautifulSoup(html, 'html.parser')
#print(soup.prettify()) 
#print(len(html))
f= open("F:\Harsh docs\python\sample.py","w")
f.write(soup.prettify())
'''
'''
url2 = 'https://www.daad.de/deutschland/studienangebote/international-programmes/en/detail/4429/'
print("Opening the file connection...")
uh2= urllib.request.urlopen(url2, context=ctx)
print("HTTP status",uh2.getcode())
html2 =uh2.read().decode()
print(f"Reading done. Total {len(html2)} characters read.") 

soup2 = BeautifulSoup(html2, 'html.parser')
f2= open("F:\Harsh docs\python\sample2.py","w")
f2.write(soup2.prettify())
'''
# for chemnitz
f= open("F:\Harsh docs\python\sample.py","r")
soup = BeautifulSoup(f, 'html.parser')

excel ={}

#Course Name
for tag in soup.find_all('span', attrs={"class":"d-none d-sm-block"}):
        excel.update({'Course Name' : tag.text.strip(" \t\n\r")})

#University
for uni in soup.find_all('h3', attrs={"class":"c-detail-header__subtitle"}):
        excel.update({'University' : uni.text.strip(" \t\n\r")})

#overview
view = soup.find('div', attrs={"aria-labelledby":"overview-tab"})            
v1  = BeautifulSoup(str(view), 'html.parser')

for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content"}))):
    excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})
print ("#################################################")
       
       
#Course Details
view = soup.find('div', attrs={"aria-labelledby":"detail-tab"})            
v1  = BeautifulSoup(str(view), 'html.parser')

for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
    #print(i.text.strip(" \t\n\r") + ":" + j.text.strip(" \t\n\r"))
    excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})
print ("#################################################")
       

 
#Costs / Funding
view = soup.find('div', attrs={"aria-labelledby":"costs-tab"})            
v1  = BeautifulSoup(str(view), 'html.parser')

for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
    #print(i.text.strip(" \t\n\r") + ":" + j.text.strip(" \t\n\r"))
    excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})
print ("#################################################")


#Requirements / Registration
view = soup.find('div', attrs={"aria-labelledby":"registration-tab"})            
v1  = BeautifulSoup(str(view), 'html.parser')

for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
    #print(i.text.strip(" \t\n\r") + ":" + j.text.strip(" \t\n\r"))
    excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})
print ("#################################################")


#Services
view = soup.find('div', attrs={"aria-labelledby":"services-tab"})            
v1  = BeautifulSoup(str(view), 'html.parser')

for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
    #print(i.text.strip(" \t\n\r") + ":" + j.text.strip(" \t\n\r"))
    excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})
print ("#################################################")
       

#convert to ordered dict and save it to csv file       
excel2 = OrderedDict(excel.items())

#for magdeburg


f= open("F:\Harsh docs\python\sample2.py","r")
soup = BeautifulSoup(f, 'html.parser')

excelmag ={}

#Course Name
for tag in soup.find_all('span', attrs={"class":"d-none d-sm-block"}):
        excelmag.update({'Course Name' : tag.text.strip(" \t\n\r")})

#University
for uni in soup.find_all('h3', attrs={"class":"c-detail-header__subtitle"}):
        excelmag.update({'University' : uni.text.strip(" \t\n\r")})

#overview
view = soup.find('div', attrs={"aria-labelledby":"overview-tab"})            
v1  = BeautifulSoup(str(view), 'html.parser')

for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content"}))):
    excelmag.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})
print ("#################################################")
       
       
#Course Details
view = soup.find('div', attrs={"aria-labelledby":"detail-tab"})            
v1  = BeautifulSoup(str(view), 'html.parser')

for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
    excelmag.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})
print ("#################################################")
       

 
#Costs / Funding
view = soup.find('div', attrs={"aria-labelledby":"costs-tab"})            
v1  = BeautifulSoup(str(view), 'html.parser')

for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
    excelmag.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})
print ("#################################################")


#Requirements / Registration
view = soup.find('div', attrs={"aria-labelledby":"registration-tab"})            
v1  = BeautifulSoup(str(view), 'html.parser')

for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
    excelmag.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})
print ("#################################################")


#Services
view = soup.find('div', attrs={"aria-labelledby":"services-tab"})            
v1  = BeautifulSoup(str(view), 'html.parser')

for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
    excelmag.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})
print ("#################################################")
       
#convert to ordered dict and save it to csv file for magdeburg       
excelmag2 = OrderedDict(excelmag.items())
pds = pd.DataFrame([excel2, excelmag2], index = [1, 2])
pds.to_csv("F:\Harsh docs\python\sample3.csv")  

