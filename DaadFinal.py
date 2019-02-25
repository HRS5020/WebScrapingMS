# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 12:32:34 2019
@author: Harsh  R . Solanki
"""

# Import all necessary libraries
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import time

from  collections import OrderedDict
from selenium import webdriver

starttime = time.time()
'''

PART - 1 - Get links of the courses of your desired category

'''

#Enter the result url from daad.de for which you need to all the course links and details    
urlpage = input('Enter Url :')
print("------------------------------------------------------------")
print("PART - 1 - Get links of the courses of your desired category")
print("------------------------------------------------------------")

#save landing page html to .py file
def courselist_html(url, pagename):
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(30)
    innerHTML = driver.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(innerHTML, 'html.parser')
    tempfile = 'F:\HarshDocs\python\WebScrapingMS\data\%s'%pagename
    f= open(tempfile,"w")
    f.write(soup.prettify())
    f.close()
    return (f.name)
    
#check how many courses are available
def number_of_courses(filename):
    f= open(filename,"r")
    soup = BeautifulSoup(str(f.read()), 'html.parser')
    view = soup.find('h2', attrs={"class":"c-result-header__title js-result-header-title"})
    result = view.text.strip(" \t\n\r").split(' ', 1)[0]
    print(result + "courses found")
    f.close()
    return(result)

#save link and course name to a directory
def extract_course_links(filename, excel):
    f= open(filename,"r")
    soup = BeautifulSoup(str(f.read()), 'html.parser')
    view = soup.find_all('a', attrs={"class":"list-inline-item mr-0 js-course-detail-link"})            
    for i in view:
        excel.append(str(i.attrs['href']))
    f.close()

rowdetails = []
totalresult = (math.ceil((int(number_of_courses(courselist_html(urlpage,"mechanical.py")))/10)))
offset = 0
links =[]

# save the links of all result pages in a list
for i in range(totalresult):
    offset = i*10
    courseurl = urlpage.replace('offset=','offset=' + str(offset))
    links.append(courseurl)

# extract all 10 course links from individual result page
for i,j in enumerate(links):
    print('Saving the html results page to ' + str(i) +'resultspage.py')
    extract_course_links(courselist_html(str(j), str(i)+'page.py'), rowdetails)
    time.sleep(30)

'''
# save the course link and course name to excel file
rowdetails2 = OrderedDict(rowdetails.items())
df = pd.DataFrame(data=rowdetails2, index=[0])
df = (df.T)
df.to_excel('F:\Harsh docs\python\Daad\courselinks.xlsx')
'''

print ("PART - 1 - Complete!!")

'''

PART - 2 - Extract all the details of particular course and add it in excel sheet

'''
print("------------------------------------------------------------")
print ("PART - 2 - Extract all the details of particular course and add it in excel sheet")
print("------------------------------------------------------------")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Get the HTML details of the course and return it as a BeautifulSoup object
def fetch_html(fullurl,contextstring, page):
    print("Opening the file connection for " + fullurl)
    uh= urllib.request.urlopen(fullurl, context=contextstring)
    print("HTTP status",uh.getcode())
    html =uh.read().decode()
    bs = BeautifulSoup(html, 'html.parser')
    coursehtml = str("F:\HarshDocs\python\WebScrapingMS\data\course"+page+".py")
    f= open(coursehtml, 'w', encoding="utf-8")
    f.write(bs.prettify())
    print("Saved to " + coursehtml)
    print("--")
    f.close()
    return bs

# Get course name and add it in a dictionary
def course_name(soup,excel):
    for tag in soup.find_all('span', attrs={"class":"d-none d-sm-block"}):
        excel.update({'Course Name' : tag.text.strip(" \t\n\r")})

# Get university name and add it in a dictionary
def university(soup,excel):
    for uni in soup.find_all('h3', attrs={"class":"c-detail-header__subtitle"}):
        excel.update({'University' : uni.text.strip(" \t\n\r")})

# Get the details listed in "overview" tab and add it in a dictionary
def overview(soup,excel):
    view = soup.find('div', attrs={"aria-labelledby":"overview-tab"})            
    v1  = BeautifulSoup(str(view), 'html.parser')

    for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content"}))):
        excel.update({str(i.text.strip(" \t\n\r\br")) : str(j.text.strip(" \t\n\r\br"))})

# Get the details listed in "course details" tab and add it in a dictionary
def course_details(soup,excel):
    view = soup.find('div', attrs={"aria-labelledby":"detail-tab"})            
    v1  = BeautifulSoup(str(view), 'html.parser')

    for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
        excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})

# Get the details listed in "Costs/funding" tab and add it in a dictionary
def costs_funding(soup,excel):
    view = soup.find('div', attrs={"aria-labelledby":"costs-tab"})            
    v1  = BeautifulSoup(str(view), 'html.parser')

    for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
        excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})

# Get the details listed in "Requirements/Regestration" tab and add it in a dictionary
def requirements_registration(soup,excel):
    view = soup.find('div', attrs={"aria-labelledby":"registration-tab"})            
    v1  = BeautifulSoup(str(view), 'html.parser')

    for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
        excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})

# Get the details listed in "Services" tab and add it in a dictionary
def services(soup,excel):
    view = soup.find('div', attrs={"aria-labelledby":"services-tab"})            
    v1  = BeautifulSoup(str(view), 'html.parser')

    for (i,j) in zip((v1.find_all('dt', attrs={"class":"c-description-list__content"})),(v1.find_all('dd', attrs={"class":"c-description-list__content mb-0"}))):
        excel.update({i.text.strip(" \t\n\r\br") : j.text.strip(" \t\n\r\br")})

# read the courselinks file
# call functions and append whole dictionary of particular course to the original list 
final_list = []    
for j,i in enumerate(rowdetails):
    time.sleep(30)
    coursecontent = {} 
    i = 'https://www.daad.de' + i
    coursecontent.update({'Link' : str(i)})
    soup_object = fetch_html(str(i),ctx, str(j))
    course_name(soup_object,coursecontent)
    university(soup_object,coursecontent)
    overview(soup_object,coursecontent)
    course_details(soup_object,coursecontent)
    costs_funding(soup_object,coursecontent)
    requirements_registration(soup_object,coursecontent)
    services(soup_object,coursecontent)
    coursecontent2 = OrderedDict(coursecontent.items())
    final_list.append(coursecontent2)
    
# save it to excel file from original list 
pds = pd.DataFrame(final_list)
pds.to_excel("F:\HarshDocs\python\WebScrapingMS\All_Details.xlsx") 
print("File has been saved to F:\HarshDocs\python\WebScrapingMS\All_Details.xlsx")
print ("PART - 2 - Complete!!")
print("------------------------------------------------------------")
print ("Your CSV file is Ready!!")
print("------------------------------------------------------------")
print("Script Finished: %.4f sec" % (time.time() - starttime))
#15 result --- https://www.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&degree%5B%5D=2&lang%5B%5D=2&fos=3&crossFac=&cert=&admReq=&scholarshipLC=&scholarshipSC=&langDeAvailable=&langEnAvailable=&lvlEn%5B%5D=&cit%5B%5D=&tyi%5B%5D=1&tyi%5B%5D=2&fee=0&bgn%5B%5D=1&dur%5B%5D=0-63070000&sort=4&ins%5B%5D=&subjects%5B%5D=15&limit=10&offset=&display=list
#03 result --- https://www.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&degree%5B%5D=2&lang%5B%5D=2&fos=3&crossFac=&cert=&admReq=&scholarshipLC=&scholarshipSC=&langDeAvailable=&langEnAvailable=&lvlEn%5B%5D=&cit%5B%5D=&tyi%5B%5D=1&fee=0&bgn%5B%5D=1&dur%5B%5D=0-63070000&sort=4&ins%5B%5D=&subjects%5B%5D=15&limit=10&offset=&display=list