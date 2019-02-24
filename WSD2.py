# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 23:40:12 2019

@author: Harsh  R . Solanki
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import csv
import time
from  collections import OrderedDict

def fetch_html(fullurl,contextstring):
    print("Opening the file connection for " + fullurl)
    uh= urllib.request.urlopen(fullurl, context=contextstring)
    print("HTTP status",uh.getcode())
    html =uh.read().decode()
    bs = BeautifulSoup(html, 'html.parser')
    return bs

def course_name(soup,excel):
    for tag in soup.find_all('span', attrs={"class":"d-none d-sm-block"}):
        excel.update({'Course Name' : tag.text.strip(" \t\n\r")})

def university(soup,excel):
    for uni in soup.find_all('h3', attrs={"class":"c-detail-header__subtitle"}):
        excel.update({'University' : uni.text.strip(" \t\n\r")})

def overview(soup,excel):
    view = soup.find('div', attrs={"aria-labelledby":"overview-tab"})            
    v1  = BeautifulSoup(str(view), 'html.parser')

    for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content"}))):
        excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})

def course_details(soup,excel):
    view = soup.find('div', attrs={"aria-labelledby":"detail-tab"})            
    v1  = BeautifulSoup(str(view), 'html.parser')

    for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
        excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})

def costs_funding(soup,excel):
    view = soup.find('div', attrs={"aria-labelledby":"costs-tab"})            
    v1  = BeautifulSoup(str(view), 'html.parser')

    for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
        excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})

def requirements_registration(soup,excel):
    view = soup.find('div', attrs={"aria-labelledby":"registration-tab"})            
    v1  = BeautifulSoup(str(view), 'html.parser')

    for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
        excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})

def services(soup,excel):
    view = soup.find('div', attrs={"aria-labelledby":"services-tab"})            
    v1  = BeautifulSoup(str(view), 'html.parser')

    for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
        excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



# read the courselinks file
#df = pd.read_excel('F:\Harsh docs\python\Daad\courselinks.xlsx')

# call functions and append whole dictionary of particular course to the original list 
final_list = []        
df = pd.read_excel('F:\Harsh docs\python\Daad\courselinks.xlsx')

for i in df['links']:
    rowdetails = {}
    print(i)
    soup = fetch_html(str(i),ctx)
    course_name(soup,rowdetails)
    university(soup,rowdetails)
    overview(soup,rowdetails)
    #course_details(soup,rowdetails)
    #costs_funding(soup,rowdetails)
    #requirements_registration(soup,rowdetails)
    #services(soup,rowdetails)
    rowdetails2 = OrderedDict(rowdetails.items())
    final_list.append(rowdetails2)
    #time.sleep(30)
    print(rowdetails2)

pds = pd.DataFrame(final_list)
pds.to_excel("F:\Harsh docs\python\Daad\All_Details.xlsx") 
print("File has been saved to F:\Harsh docs\python\All_Details.xlsx")
