from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

from Select_Course_Section import SelectSection
from Select_Semester import SelectSemester


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
    s = SelectSemester(session=year + ' ' + semester, soup=soup, driver=driver)
    section_table = s.select_session()
    # section_table = soup.find('table', {'bgcolor': 'white'})
    tr_table = section_table.find_all('tr')
    for i in range(len(tr_table)):
        print(i, len(tr_table))
        s = SelectSection(P_Period='P1', driver=driver)
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
p_period = input("For what period would you like totals, P1, P2, P3, or Grand Total? ")
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
