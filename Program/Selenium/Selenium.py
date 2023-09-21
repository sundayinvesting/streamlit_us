# import webdriver
import os
import time

Dir=r'C:\edgedriver_win64'

os.chdir(Dir)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
options = webdriver.EdgeOptions()
options.use_chromium = True
driver = webdriver.Edge()
action = ActionChains(driver)

# Base Functions
def AddElement(ind, dat):
    element = driver.find_element(by=By.NAME, value="transaction" + str(ind))
    element.click()
    element.send_keys('Add Existing')
    element = driver.find_element(by=By.NAME, value="reltype" + str(ind))
    element.click()
    element.send_keys(dat[0])
    element = driver.find_element(by=By.NAME, value="findnum" + str(ind))
    element.click()
    element.send_keys(dat[1])
    if dat[2] != "":
        element = driver.find_element(by=By.NAME, value="qty" + str(ind))
        element.click()
        element.send_keys(dat[2])
    element = driver.find_element(by=By.NAME, value="type" + str(ind))
    element.click()
    element.send_keys(dat[3])
    element = driver.find_element(by=By.NAME, value="name" + str(ind))
    element.click()
    element.send_keys(dat[4])

def xpath_click(inp):
    while True:
        try:
            element = driver.find_element(by=By.XPATH, value=inp)
            element.click()
            break
        except:
            pass
    return

def id_click(inp):
    while True:
        try:
            element = driver.find_element(by=By.ID, value=inp)
            element.click()
            break
        except:
            pass
    return

def xpath_type(inp, str, clr):
    while True:
        try:
            element = driver.find_element(by=By.XPATH, value=inp)
            element.click()
            break
        except:
            pass
    if clr == True:
        element.clear()
    element.send_keys(str)
    return

def xpath_gettext(inp):
    while True:
        try:
            element = driver.find_element(by=By.XPATH, value=inp)
            break
        except:
            pass
    return str(element.text)

def css_gettext(inp):
    while True:
        try:
            element = driver.find_element(by=By.CSS_SELECTOR, value=inp)
            break
        except:
            pass
    return str(element.text)


def xpath_press_button(inp):
    element = driver.find_element(by=By.XPATH, value=inp)
    element.click()
    while True:
        try:
            chk = element.is_enabled()
            if chk == False:
                time.sleep(1)
                break
        except:
            break

def urlopen(url,min):
    if min == True:
        driver.minimize_window()
    if url == "lookup":
        driver.get("https://cwiprod.corp.halliburton.com/cwi/AdvLookup.jsp")
        while True:
            try:
                element = driver.find_element(by=By.XPATH, value="//tr[3]/td[2]/input")
                element.click()
                element.clear()
                break
            except:
                pass
    else:
        driver.get(url)


urlopen("https://www.nseindia.com/companies-listing/corporate-filings-insider-trading",False)
time.sleep(2)
xpath_click("//div[2]/div/div/div/div/ul/li[2]/a")
while True:
    print("Wait")



