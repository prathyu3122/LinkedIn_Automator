from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import requests
import docx2txt
import re
import os
import shutil


driver = webdriver.Chrome()
 
driver.get('https://www.linkedin.com')
 
username = driver.find_element_by_id('session_key')
uname = input("Enter your username: ")

# Username will be taken here
username.send_keys(uname)

Password = input("Enter your password: ")
 
password = driver.find_element_by_id('session_password')
 
# Password will be taken here
password.send_keys(Password)

log_in = driver.find_element_by_class_name('sign-in-form__submit-button')
 
log_in.click()

# Jobs url should be given here.

job_url = input("Enter your Job URL here: ") 
driver.get(job_url)

html = driver.page_source

soup = BeautifulSoup(html,'lxml')


# Getting into each page
Pagination =soup.select("div[class='pv5 artdeco-pagination ember-view'] > ul > li[id^='ember'] > button")

for p in range(1,len(Pagination)+1):
    page = driver.find_element_by_css_selector("div[class='pv5 artdeco-pagination ember-view'] > ul > li[id^='ember']:nth-child(" + str(p) + ")")
    page.click()  
    
    html = driver.page_source
 
    soup = BeautifulSoup(html,'lxml')

    Applicants=[]
    
    Class = soup.findAll('li', {'class': 'hiring-applicants__list-item'})
    
    for Sub in Class:
    
        Applicants.append('https://www.linkedin.com'+str(Sub.find("a").get('href')))

    applicant_details=[]
    
    
    for i in Applicants:
    
        driver.get(i)
    
        html = driver.page_source
    
        soup = BeautifulSoup(html,'lxml')

    
        Profile = soup.findAll('div', {'class': 'hiring-profile-highlights__see-full-profile'})
    
        for Sub in Profile:
    
            Profile_Url='https://www.linkedin.com'+str(Sub.find("a").get('href'))
    
            applicant_details.append(Profile_Url)
    

        html = driver.page_source
    
        soup = BeautifulSoup(html,'lxml')
    
        #print(applicant_details)


        Profile = soup.findAll('div', {'class': 'hiring-profile-highlights__see-full-profile'})
        for Sub in Profile:
            n = str(Sub.find("a").get('href'))
            applicant_name = n[4:len(n)-1]
            Resume_pdf = applicant_name + ".pdf"
        
        print(Resume_pdf)

        #Getting resumes into a list
        Resumes = soup.findAll('div', {'class': ['hiring-resume-viewer__resume-wrapper--collapsed','ui-attachment ui-attachment--doc']})
        #urls = []

        for x in Resumes:
    
            resume_url = str(x.find("a").get("href"))
            #resume_urls.append(url)
            req = requests.get(resume_url)
            with open(Resume_pdf, 'wb') as f:
                for chunk in req.iter_content(chunk_size = 8192):
                    if(chunk):
                        f.write(chunk)
        

# For storing Resumes in a new dir
os.mkdir("All_Resumes")


# List of all pdf files in current directory
arr = [x for x in os.listdir() if x.endswith(".pdf")]

for k in arr:
    shutil.move(k,"All_Resumes")


