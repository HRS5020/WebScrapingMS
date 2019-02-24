import re
import urllib.request, urllib.parse, urllib.error
import ssl
import time
import pandas as pd
import math
from selenium import webdriver
from bs4 import BeautifulSoup
from  collections import OrderedDict

#Enter the result url for which you need to all the course links and details    
#urlpage ='https://www.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&degree%5B%5D=2&lang%5B%5D=2&fos=3&crossFac=&cert=&admReq=&scholarshipLC=&scholarshipSC=&langDeAvailable=&langEnAvailable=&lvlEn%5B%5D=&cit%5B%5D=&tyi%5B%5D=2&fee=0&bgn%5B%5D=1&dur%5B%5D=&sort=4&ins%5B%5D=&subjects%5B%5D=15&limit=10&offset=&display=list'
urlpage = input('Enter Url :')
print(urlpage)

#save landing page html to .py file
def courselist_html(url, pagename):
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(30)
    innerHTML = driver.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(innerHTML, 'html.parser')
    tempfile = 'F:\Harsh docs\python\Daad\%s'%pagename
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
    print(result)
    print("--------------------------------------")
    f.close()
    return(result)

#save link and course name to a directory
def extract_course_links(filename, excel):
    f= open(filename,"r")
    soup = BeautifulSoup(str(f.read()), 'html.parser')
    view = soup.find_all('a', attrs={"class":"list-inline-item mr-0 js-course-detail-link"})            
    for i in view:
        excel.update({i.attrs['href'] : i.text.strip(" \t\n\r")})
    f.close()

rowdetails = {'Link':'Course Name'}
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
    print('saving the html page of to ' + str(i) +'page.py')
    extract_course_links(courselist_html(str(j), str(i)+'page.py'), rowdetails)
    time.sleep(60)

# save the course link and clurse name to excel file
rowdetails2 = OrderedDict(rowdetails.items())
df = pd.DataFrame(data=rowdetails, index=[0])
df = (df.T)
df.to_excel('F:\Harsh docs\python\Daad\courselinks.xlsx')