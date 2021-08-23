import selenium
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


class SelectSession(object):
    # driver = webdriver.Chrome("C:/Users/53674/PycharmProjects/chromedriver.exe")

    def __init__(self, session):
        self.session = session

    def select_session(self):
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        table = soup.find('select', {'onchange': 'New_Term(this.form)', 'name': 'term_code'})
        option_table = table.find_all('option')
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        # for i in range(len(option_table)):
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        print('Hello, the session is', self.session)
        table = soup.find('select', {'onchange': 'New_Term(this.form)', 'name': 'term_code'})
        option_table = table.find_all('option')

        for i in range(len(option_table)):
            semester = option_table[i].text
            if semester == self.session:
                y = i + 1
                print(f'y = {i + 1}')
                drop_down = driver.find_element_by_xpath(
                    '/html/body/table[2]/tbody/tr/td[2]/form[1]/p/select/option[' + str(y) + ']').click()
                # This waits for list of courses to load
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'clform')))
                page_source = driver.page_source
                soup2 = BeautifulSoup(page_source, 'lxml')
                section_table = soup2.find('table', {'bgcolor': 'white'})
                return section_table
                break


class SelectSection:

    def __init__(self, P_Period):
        self.P_Period = P_Period

    def selection_process(self, i):

        def completion_date_formatting():
            button2 = driver.find_element_by_xpath(
                '//*[@id="clform"]/table/tbody/tr[' + str(i) + ']/td[1]/input').click()
            # This waits until roster open to run
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'college')))
            # This clicks on final grades link
            course_date = driver.find_element_by_xpath(
                '/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[4]/td[3]').text
            course_date_split = course_date.split()
            return course_date_split

        def section_number_formatting():
            global section_and_course
            course = driver.find_element_by_xpath(
                '/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[2]/td[3]').text
            cutup = course.split()
            for word in cutup:
                if "(" in word:
                    section = word
                    # section = cutup[4]
                    section = section[1:]
            course2 = cutup[0] + ' ' + cutup[1][:5]
            return section, course2

        global section_and_course
        counted_course = driver.find_element_by_xpath('//*[@id="clform"]/table/tbody/tr[' + str(i) + ']/td[2]').text
        print(counted_course)
        if (counted_course != "AED 40.01") and ("IWAP" not in counted_course):
            section_and_course = 0
            pass
        else:
            course_date_split = completion_date_formatting()
            if self.P_Period == "P1":
                p1_eligible_months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                if course_date_split[9] in p1_eligible_months:
                # if course_date_split[9] == 'Aug' or course_date_split[9] == 'Jul' or course_date_split[9] == \
                #         'Nov' or course_date_split[9] == 'Dec':
                    section_and_course = section_number_formatting()
                    print(section_and_course)
                elif course_date_split[10] in p1_eligible_months:
                # elif course_date_split[9] == 'Aug' or course_date_split[10] == 'Jul' or course_date_split[10] == \
                #         'Nov' or course_date_split[10] == 'Dec':
                    section_and_course = section_number_formatting()
                    print(section_and_course)
                elif course_date_split[11] in p1_eligible_months:
                # elif course_date_split[9] == 'Aug' or course_date_split[11] == 'Jul' or course_date_split[11] == \
                #         'Nov' or course_date_split[11] == 'Dec':
                    section_and_course = section_number_formatting()
                    print(section_and_course)
                else:
                    driver.back()
            elif self.P_Period == "P2":
                if course_date_split[9] == 'Apr' or course_date_split[9] == 'May':
                    section_and_course = section_number_formatting()
                    print(section_and_course)
                elif course_date_split[10] == 'Apr' or course_date_split[10] == 'May':
                    section_and_course = section_number_formatting()
                    print(section_and_course)
                else:
                    driver.back()
            elif self.P_Period == "P3":
                if course_date_split[9] == 'Apr' or course_date_split[9] == 'May' or course_date_split[9] == 'Jun':
                    section_and_course = section_number_formatting()
                    print(section_and_course)
                elif course_date_split[10] == 'Apr' or course_date_split[10] == 'May' or course_date_split[9] == 'Jun':
                    section_and_course = section_number_formatting()
                    print(section_and_course)
                else:
                    driver.back()
                    section_and_course = 0
            return section_and_course


class RawDataHours:
    global df_raw_section_data

    def __init__(self, section, course2):
        self.section = section
        self.course2 = course2

    def raw_data_hours(self):

        def table3_function():
            table3 = table.find_all('tr')[1:]
            for j in table3:
                raw_section_data = j.find_all('td')
                row = [tr.text for tr in raw_section_data]
                row.append(self.section)
                row.append(self.course2)
                try:
                    length = len(df_raw_section_data)
                    df_raw_section_data.loc[length] = row
                except:
                    continue
            driver.back()
            driver.back()

        headers = ['NO', 'Name', 'ID', 'Grade', 'Hours', 'Other', 'Section', 'Course']
        df_raw_section_data = pd.DataFrame(columns=headers)
        final_hours = driver.find_element_by_xpath('//*[@id="FinalGrades_form"]/a').click()
        course = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[2]/td[3]').text
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Roster_form')))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        table = soup.find('table', {'bgcolor': 'white', 'cellpadding': '5', 'cellspacing': '0'})
        try:
            table2 = table.find_all('th')
            table3_function()

        except:
            driver.back()
            driver.back()

        return df_raw_section_data


class TotalSectionHours:
    headers2 = ['Course', 'Section', 'Total']
    df_sections = pd.DataFrame(columns=headers2)
    length = 0

    def __init__(self, df_raw_section_data):
        self.df_raw_section_data = df_raw_section_data

    def total_section_hours(self):
        course = 0
        section = 0
        total_hours = 0
        section_hours = []
        print('length equals', TotalSectionHours.length)
        for i in range(len(self.df_raw_section_data)):
            section = self.df_raw_section_data.loc[i, 'Section']
            course = self.df_raw_section_data.loc[i, 'Course']
            hours = self.df_raw_section_data.loc[i, 'Hours']
            hours = hours.split()
            hours = hours[0]
            if hours == 'hours':
                hours = 0
            hours = float(hours)
            total_hours = total_hours + hours
        section_hours.append(course)
        section_hours.append(section)
        section_hours.append(total_hours)
        TotalSectionHours.df_sections.loc[TotalSectionHours.length] = section_hours
        TotalSectionHours.length = TotalSectionHours.length + 1
        print('df sections', TotalSectionHours.df_sections)
        TotalSectionHours.df_sections.to_csv('C:/Users/family/Desktop/IWPA_Section_Totals.csv')
        # return TotalSectionHours.df_sections


def calculate_apprecticeship_hours(year, semester):

    global section_and_course
    global tr_table
    global df_sections
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    table = soup.find('select', {'onchange': 'New_Term(this.form)', 'name': 'term_code'})
    option_table = table.find_all('option')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    # for i in range(len(option_table)):
    p = SelectSession(session=year + ' ' + semester)
    section_table = p.select_session()
    # section_table = soup.find('table', {'bgcolor': 'white'})
    tr_table = section_table.find_all('tr')
    for i in range(len(tr_table)):
        print(i, len(tr_table))
        s = SelectSection(P_Period='P1')
        section_and_course = s.selection_process(i + 1)
        print(section_and_course)
        if section_and_course == None:
            continue
        r = RawDataHours(section=section_and_course[0], course2=section_and_course[1])
        df_raw_section_data = r.raw_data_hours()
        df_empty = df_raw_section_data.empty
        if df_empty == True:
            continue
        t = TotalSectionHours(df_raw_section_data)
        t.total_section_hours()





p_period = input("For what period would you like totals, P1, P2, P3, or Grand Total? ")
driver = webdriver.Chrome("C:/Users/family/PycharmProjects/chromedriver.exe")
driver.get('https://secure.cerritos.edu/rosters/login.cgi')
login = driver.find_element_by_name('login')
login.send_keys('gvasquez')
login = driver.find_element_by_name('passwd')
login.send_keys('Celestino80!')
button = driver.find_element_by_xpath('//*[@id="login_form"]/table/tbody/tr[3]/td[2]/input').click()
# This waits for list of courses to load
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'clform')))
# headers = ['NO', 'Name', 'ID', 'Grade', 'Hours', 'Other', 'Section', 'Course']
# df = pd.DataFrame(columns=headers)
pd.set_option('display.max_columns', None)
if p_period == "P1":
    year = input("Please provide the P1 year,e.g. 2020: ")
    calculate_apprecticeship_hours(year=year, semester='Summer')
    calculate_apprecticeship_hours(year=year, semester='Fall')
# if p_period == "P2":
#     P2_function()
# if p_period == "P3":
#     P3_function()
# if p_period == "Grand Total":
#     P1_function()
#     P3_function()



# df_raw_section_data.to_csv('C:/Users/family/Desktop/IWPA_Raw_Data.csv')
# df_sections.to_csv('C:/Users/family/Desktop/IWPA_Section_Totals.csv')
