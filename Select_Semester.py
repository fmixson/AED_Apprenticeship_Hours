from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class SelectSemester:

    def __init__(self, session, soup, driver):
        # self.chromedriver = chromedriver
        self.session = session
        self.soup = soup
        self.driver = driver

    def select_session(self):

        table = self.soup.find('select', {'onchange': 'New_Term(this.form)', 'name': 'term_code'})
        option_table = table.find_all('option')

        for i in range(len(option_table)):
            semester = option_table[i].text
            if semester == self.session:
                y = i + 1
                print(f'y = {i + 1}')
                drop_down = self.driver.find_element_by_xpath(
                    '/html/body/table[2]/tbody/tr/td[2]/form[1]/p/select/option[' + str(y) + ']').click()
                # This waits for list of courses to load
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'clform')))
                page_source = self.driver.page_source
                soup2 = BeautifulSoup(page_source, 'lxml')
                section_table = soup2.find('table', {'bgcolor': 'white'})
                return section_table
