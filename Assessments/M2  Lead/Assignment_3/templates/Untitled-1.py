
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup

import scrapy
from scrapy import spider
from scrapy.spiders import CrawlSpider, Rule
import yaml
import getpass
import time
from selenium import webdriver

import json
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import pandas as pd
import csv
import tfidf

driver = webdriver.Chrome(executable_path='/Users/williamzhou/Desktop/chromedriver')
driver.get("https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=data+scientist&sc.keyword=data+scientist&locT=&locId=&jobType=")
info =[]
location = [
    'Atlanta, GA','Austin, TX','Boston, MA',
            'Cambridge, MA','Chicago, IL','Los Angeles, CA',
            'New York, NY','Palo Alto, CA','Philadelphia, PA',
            'San Diego, CA','San Francisco, CA','San Jose, CA',
            'Seattle, WA',
            'Washington, DC','TX'
]
# get the link of each job post
jobname = driver.find_element_by_name('sc.keyword')
jobname.clear()
jobname.send_keys('data scientist')
joblk=[]

for loc in location:
    locsc = driver.find_element_by_id('sc.location')
    locsc.clear()
    locsc.send_keys(loc)
    driver.find_element_by_xpath('//*[@id="SiteSrchTop"]/form/button').click()
    time.sleep(3)

    for i in range(33):
        try:
            
            for ele in driver.find_elements_by_xpath('//*[@id="MainCol"]/ul/li'):
                salalk={}
                salalk['link']=ele.find_element_by_xpath('./div[2]/div[1]/div[1]/a').get_attribute('href')
                salalk['location'] = ele.find_element_by_xpath('//*[@id="HeroHeaderModule"]/div[3]/div[2]/div/div[1]/span[2]').text
                
                try: 
                    salalk['salary'] = ele.find_element_by_xpath('./div[2]/div[3]/div[1]/span').text
                except NoSuchElementException:
                    salalk['salary'] = None 
                joblk.append(salalk)
            try:
                driver.find_element_by_xpath('//*[@id="FooterPageNav"]/div/ul/li[7]/a').click()
            except WebDriverException:
                driver.find_element_by_xpath('//*[@id="JAModal"]/div/div/div[2]/div/button').click()

            print 'scraping %s' %loc
            print 'page %d' %(i+1)

        except NoSuchElementException or WebDriverException:
            try:
                driver.find_element_by_xpath('//*[@id="JAModal"]/div/div/div[2]/div/button').click()
            except NoSuchElementException:
                print "%s finished" %loc
        
        time.sleep(2)
            
    with open('/Users/williamzhou/Desktop/glassdoor/%s.json'%loc.replace(', ',''), 'w') as fp:
        json.dump(joblk, fp)

        
link = salalk['link']    
info=[]
page = webdriver.Chrome(executable_path='/Users/williamzhou/Desktop/chromedriver')
for lk in link:
    try:
        page.get(lk)
        time.sleep(4)
        info_detail ={}
        info_detail['i']=i
        info_detail['link'] = lk
        info_detail['jobtitle'] = [x.text for x in page.find_elements_by_xpath('//*[@id="HeroHeaderModule"]/div[3]/div[2]/h2')]
        info_detail['employername'] =[x.text for x in page.find_elements_by_xpath('//*[@id="HeroHeaderModule"]/div[3]/div[2]/span[1]')]
        info_detail['employerlocation'] = [x.text for x in page.find_elements_by_xpath('//*[@id="HeroHeaderModule"]/div[3]/div[2]/span[2]')]
        info_detail['jobdescp'] = [x.text for x in page.find_elements_by_xpath('//*[@id="JobDescContainer"]')]
        info_detail['hq'] = [x.text for x in page.find_elements_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div[2]/span')]
        info_detail['companysize'] = [x.text for x in page.find_elements_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div[3]/span')]
        info_detail['founded'] = [x.text for x in page.find_elements_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div[4]/span')]
        info_detail['companytype'] = [x.text for x in page.find_elements_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div[5]/span')]
        info_detail['industry'] = [x.text for x in page.find_elements_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div[6]/span')]
        info_detail['revenue'] = [x.text for x in page.find_elements_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div[7]/span')]
        info.append(info_detail)
        time.sleep(2)
        print i+1
        i=i+1
    except:
        with open('/Users/williamzhou/Desktop/glassdoor/scrape_to_%d.json'%(i+1), 'w') as fp:
            json.dump(info, fp)
with open('/Users/williamzhou/Desktop/glassdoor/scrape_to_%d.json'%(i+1), 'w') as fp:
    json.dump(info, fp)