from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

class FaceBot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        options.add_argument("--lang=en-US")
        self.browser = webdriver.Chrome(executable_path="chromedriver.exe",options=options)
    
    def signup(self,email,password,person):
        if self.browser.current_url != "https://facebook.com/reg":
            self.browser.get("https://facebook.com/reg")
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.NAME, "firstname"))).send_keys(person.fname)
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.NAME, "lastname"))).send_keys(person.lname)
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.NAME, "reg_email__"))).send_keys(email)
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.NAME, "reg_email_confirmation__"))).send_keys(email)
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.NAME, "reg_passwd__"))).send_keys(password)
        birthday_day = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.NAME, "birthday_day")))
        birthday_month = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.NAME, "birthday_month")))
        birthday_year = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.NAME, "birthday_year")))
        Select(birthday_day).select_by_value(person.day)
        Select(birthday_month).select_by_value(person.month)
        Select(birthday_year).select_by_value(person.year)
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@value='"+str(person.gender)+"']"))).click()
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.NAME, "websubmit"))).click()
        WebDriverWait(self.browser,20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Continue']"))).click()

    def logout(self):
        self.browser.delete_all_cookies()
        self.browser.execute_script('window.localStorage.clear();')
        self.browser.execute_script('window.sessionStorage.clear();')
        self.browser.get("https://facebook.com/reg")

    def close(self):
        self.browser.close()