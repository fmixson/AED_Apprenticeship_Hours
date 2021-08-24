from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# from AED import driver


class SelectSection:

    def __init__(self, P_Period, driver):
        self.P_Period = P_Period
        self.driver = driver

    def selection_process(self, i):

        def completion_date_formatting():
            button2 = self.driver.find_element_by_xpath(
                '//*[@id="clform"]/table/tbody/tr[' + str(i) + ']/td[1]/input').click()
            # This waits until roster open to run
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'college')))
            # This clicks on final grades link
            course_date = self.driver.find_element_by_xpath(
                '/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[4]/td[3]').text
            course_date_split = course_date.split()
            return course_date_split

        def section_number_formatting():
            global section_and_course
            course = self.driver.find_element_by_xpath(
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
        counted_course = self.driver.find_element_by_xpath('//*[@id="clform"]/table/tbody/tr[' + str(i) + ']/td[2]').text
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
                    self.driver.back()
            elif self.P_Period == "P2":
                if course_date_split[9] == 'Apr' or course_date_split[9] == 'May':
                    section_and_course = section_number_formatting()
                    print(section_and_course)
                elif course_date_split[10] == 'Apr' or course_date_split[10] == 'May':
                    section_and_course = section_number_formatting()
                    print(section_and_course)
                else:
                    self.driver.back()
            elif self.P_Period == "P3":
                if course_date_split[9] == 'Apr' or course_date_split[9] == 'May' or course_date_split[9] == 'Jun':
                    section_and_course = section_number_formatting()
                    print(section_and_course)
                elif course_date_split[10] == 'Apr' or course_date_split[10] == 'May' or course_date_split[9] == 'Jun':
                    section_and_course = section_number_formatting()
                    print(section_and_course)
                else:
                    self.driver.back()
                    section_and_course = 0
            return section_and_course