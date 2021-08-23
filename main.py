import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
driver = webdriver.Chrome("C:/Users/family/PycharmProjects/chromedriver.exe")
driver.get('https://secure.cerritos.edu/rosters/login.cgi')
login = driver.find_element_by_name('login')
login.send_keys('fmixson')
login = driver.find_element_by_name('passwd')
login.send_keys('Frankgrace129!')
button = driver.find_element_by_xpath('//*[@id="login_form"]/table/tbody/tr[3]/td[2]/input').click()
#This waits for list of courses to load
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'clform')))

no_syllabus = []
yes_syllabus = []
instructors = []

for i in range(110, 115):
    # This clicks on radio button to open roster
    button2 = driver.find_element_by_xpath('//*[@id="clform"]/table/tbody/tr['+str(i)+']/td[1]/input').click()
    # This waits until roster open to run
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'college')))
    instructor = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[1]/td[3]').text
    course = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[2]/td[3]').text
    # This clicks on syllabus to upload syllabus
    syllabus = driver.find_element_by_xpath('//*[@id="Syllabus_form"]/a').click()
    # This waits until syllabus upload page loads
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'DownloadRoster_form')))
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    # print(soup.find('input', {'type': 'file'}))
    check_for_syllabus = soup.find('input', {'type': 'file'})
    # print(check_for_syllabus)
    if check_for_syllabus == None:
        yes_syllabus.append(course)
    else:
        no_syllabus.append(course)
        instructors.append(instructor)
    driver.back()
    driver.back()
# print(yes_syllabus)
# print(no_syllabus)
section = []
column = ['Section']
df = pd.DataFrame(columns=column)






    # uploaded = soup.find_all('syllabus1')
    # print(uploaded)
    # upload = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/form/div/table/tbody/tr[2]/td/input')
    # print(course)
    # if driv'/html/body/table/tbody/tr/td[2]/form/div/table/tbody/tr[2]/td/input' == "file":
    # names = driver.find_element_by_name('syllabus1')
    # print(names)
    # if names == 'syllabus1':
    #     no_syllabus.append(course)
    #     print(no_syllabus)
    # else:
    #     yes_syllabus.append(course)

# button2 = driver.find_element_by_xpath('//*[@id="clform"]/table/tbody/tr[1]/td[1]/input').click()

# url = 'https://secure.cerritos.edu/rosters/class_list.cgi'
# page = requests.get(url)
# list_of_courses = BeautifulSoup(page.text,'lxml')
# print(list_of_courses)