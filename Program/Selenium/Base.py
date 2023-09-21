import os
import time
import openpyxl
import pyperclip
import pandas as pd
import glob
#Selenium Imports
Dir=r'C:\Users\H262630\OneDrive - Halliburton\Desktop\Automation Scripts\Selenium\edgedriver_win64'
tempdir=r'C:\Users\H262630\OneDrive - Halliburton\MSeGa_WorkFIles\CWI\Automation\Temp'
os.chdir(Dir)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
options = webdriver.EdgeOptions()
options.use_chromium = True
driver = webdriver.Edge()
action = ActionChains(driver)

#Selenium low Functions-------------------------------------------------------------------------------------------------

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
#Selenium High Functions-----------------------------------------------------------------------------------------------

def Revise(PN,R):
    liv=False
    while True:
        try:
            element = driver.find_element(by=By.XPATH, value="//tr[3]/td[2]/input")
            element.click()
            element.clear()
            element.send_keys(PN)
            break
        except:
            pass
    element = driver.find_element(by=By.XPATH, value="//tr[4]/td[2]/input")
    element.click()
    element.clear()
    element.send_keys(R)
    element = driver.find_element(by=By.XPATH, value="//td[2]/table/tbody/tr/td/input")
    element.click()
    element = driver.find_element(by=By.XPATH, value="//td[3]/input")
    element.click()
    #Revised Part-----------------------
    idref = 0
    count = 1
    #identifyng the Index
    while True:
        try:
            time.sleep(1)
            element = driver.switch_to.alert
            element.accept()
            liv = True
            break
        except Exception as e:
            if str(e)[:22] == "Message: no such alert":
                try:
                    element = driver.find_element(by=By.XPATH, value="//tr[17]/td/b")
                    break
                except:pass
    return liv

def AddElement(ind,dat):
    element = driver.find_element(by=By.NAME, value="transaction" + str(ind))
    element.click()
    element.send_keys('Add Existing')
    element = driver.find_element(by=By.NAME, value="reltype" + str(ind))
    element.click()
    element.send_keys(dat[0])
    element = driver.find_element(by=By.NAME, value="findnum" + str(ind))
    element.click()
    element.send_keys(dat[1])
    if dat[2]!="":
        element = driver.find_element(by=By.NAME, value="qty" + str(idref))
        element.click()
        element.send_keys(dat[2])
    element = driver.find_element(by=By.NAME, value="type" + str(ind))
    element.click()
    element.send_keys(dat[3])
    element = driver.find_element(by=By.NAME, value="name" + str(ind))
    element.click()
    element.send_keys(dat[4])

def AddDesc(inp):
    while True:
        try:
            element = driver.find_element(by=By.XPATH, value="//div/table/tbody/tr/td[5]")
            element.click()
            break
        except:
            pass

    while True:
        try:
            element = driver.find_element(by=By.XPATH, value="//tr[3]/td/table/tbody/tr/td/textarea")
            element.click()
            break
        except:
            pass
        try:
            element = driver.find_element(by=By.XPATH, value="//tr[2]/td/table/tbody/tr/td/textarea")
            element.click()
            break
        except:
            pass
    element.send_keys(inp)
    element = driver.find_element(by=By.XPATH, value="//div[3]/div/form/table[2]/tbody/tr[2]/td[2]/input")
    element.click()
    while True:
        element = driver.find_element(by=By.XPATH, value="//div[3]/div/form/table[2]/tbody/tr[2]/td[2]/input")
        try:
            chk = element.is_enabled()
            if chk == False:
                break
        except:
            break
    return

def AddTask(inp):
    element = driver.find_element(by=By.XPATH, value="//td[7]")
    element.click()
    time.sleep(1)
    while True:
        try:
            element = driver.find_element(by=By.XPATH, value="//div[4]/div/form/table/tbody/tr[2]/td/select")
            element.click()
            break
        except:
            pass
    element.send_keys("Add Connection")
    element = driver.find_element(by=By.XPATH, value="//div[4]/div/form/table/tbody/tr[2]/td[2]/input")
    element.click()
    element.send_keys(inp)
    element = driver.find_element(by=By.XPATH, value="//div[4]/div/form/table[2]/tbody/tr[2]/td[2]/input")
    element.click()
    while True:
        element = driver.find_element(by=By.XPATH, value="//div[4]/div/form/table[2]/tbody/tr[2]/td[2]/input")
        try:
            chk = element.is_enabled()
            if chk == False:
                break
        except:
            break
    return

def TiffGen():

    while True:
        try:
            element = driver.find_element(by=By.XPATH, value="//td[9]")
            element.click()
            break
        except:
            pass
    while True:
        try:
            xpath_click("//div[5]/div/form/table/tbody/tr[3]/td/input")
            break
        except Exception:
            pass
    while True:
        try:
            xpath_click("//table[3]/tbody/tr[2]/td[2]/input")
            break
        except:
            pass
    while True:
        element = driver.find_element(by=By.XPATH, value="//table[3]/tbody/tr[2]/td[2]/input")
        try:
            chk = element.is_enabled()
            if chk == False:
                break
        except:
            break
    return

def idrefcheck(idref):
    if idref > 14:
        count += 1
        #print("15 more elements")
        element = driver.find_element(by=By.XPATH, value="//input[11]")
        element.click()
        while True:
            time.sleep(1)
            element = driver.find_element(by=By.XPATH, value="//tr[17]/td/b")
            chk = element.text
            # print(chk)
            if chk[5] == str(count):
                break
        idref = 0
    return

def delete(PN,R):
    driver.get(r"https://cwiprod.corp.halliburton.com/cwi/CreateObjectWithoutAttrs.jsp?pageType=Delete")
    while True:
        try:
            element = driver.find_element(by=By.XPATH, value="//select")
            break
        except:
            pass
    element.click()
    element.send_keys("Part")
    element.click()
    element = driver.find_element(by=By.XPATH,
                                  value="//div[@id='MenuDiv']/form/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input")
    element.click()
    element.send_keys(PN)
    element = driver.find_element(by=By.XPATH,
                                  value="//div[@id='MenuDiv']/form/table/tbody/tr/td/table/tbody/tr[4]/td[2]/input")
    element.click()
    element.send_keys(R)
    element = driver.find_element(by=By.XPATH,
                                  value="//div[@id='MenuDiv']/form/table/tbody/tr/td/table/tbody/tr[10]/td[3]/input")
    element.click()
    while True:
        try:
            element = driver.switch_to.alert
            element.accept()
            break
        except:
            pass

    return

def SwapFindCheck():
    var = 2
    time.sleep(2)
    findlist = []
    namelist = []
    time.sleep(2)
    while True:
        try:
            element = driver.find_element(by=By.XPATH, value="//div/a")
            action = ActionChains(driver)
            action.context_click(element).perform()
            element = driver.find_element(by=By.LINK_TEXT, value="Swap Find Numbers")
            element.click()
            break
        except:
            pass
    ch_window = driver.window_handles[1]
    driver.switch_to.window(ch_window)
    while True:
        try:
            name = driver.find_element(by=By.XPATH, value="//tr[%s]/td[6]" % var)
            break
        except:pass
    while True:
        try:
            name = driver.find_element(by=By.XPATH, value="//tr[%s]/td[6]" % var)
            find = driver.find_element(by=By.XPATH, value="//tr[%s]/td[2]/input" % var)
            findlist.append(find.get_attribute("value"))
            namelist.append(name.text)
            var += 1
        except:
            break
    #print(findlist, namelist)
    xvar, Pvar, Hvar, Svar, Evar =None,None,None,None,None
    for step in namelist:
        try:
            temp = step.split(",")
            if temp[0] == "TUBE":
                xvar = namelist.index(step) + 2
            if temp[0] == "PLATE":
                xvar = namelist.index(step) + 2
            if temp[0] == "PAINT":
                Pvar = namelist.index(step) + 2
            if temp[1] == " HUB":
                Hvar = namelist.index(step) + 2
            if temp[1] == " SKIRT":
                Svar = namelist.index(step) + 2
            if temp[1] == " EYE":
                Evar = namelist.index(step) + 2
        except:
            pass
    #print(xvar, Pvar, Hvar, Svar)
    if Hvar!=None:
        element = driver.find_element(by=By.XPATH, value="//tr[%s]/td/input" % Hvar)
        element.clear()
        Hvarf=xvar + 1
        element.send_keys(str(Hvarf).zfill(4))
        xvar+=1
    if Svar!=None:
        element = driver.find_element(by=By.XPATH, value="//tr[%s]/td/input" % Svar)
        element.clear()
        Svarf=xvar + 1
        element.send_keys(str(Svarf).zfill(4))
        xvar+=1
    if Evar!=None:
        element = driver.find_element(by=By.XPATH, value="//tr[%s]/td/input" % Evar)
        element.clear()
        Evarf=xvar + 1
        element.send_keys(str(Evarf).zfill(4))
        xvar+=1
    if Pvar!=None:
        element = driver.find_element(by=By.XPATH, value="//tr[%s]/td/input" % Pvar)
        element.clear()
        Pvarf = xvar + 1
        element.send_keys(str(Pvarf).zfill(4))

    element = driver.find_element(by=By.XPATH, value="//form/input")
    element.click()
    ch_window = driver.window_handles[0]
    driver.switch_to.window(ch_window)
    while True:
        try:
            time.sleep(1)
            element = driver.find_element(by=By.XPATH, value="//tr[17]/td/b")
            break
        except:
            pass
    return [Hvarf,Svarf,Pvarf,Evarf]

def lookup(PN,R,type):
    xpath_type('//td[2]/input',PN,True)
    if R != True:
        xpath_type('//tr[11]/td[2]/input',R, True)
    else:
        xpath_click("//tr[11]/td[4]/input")
    xpath_type("//tr[7]/td[2]/input",type,True)
    xpath_type('//tr[16]/td[2]/input',"SEP", True)
    xpath_click("//tr[7]/td[3]/input")

    while True:
        try:
            ch_window = driver.window_handles[1]
            driver.switch_to.window(ch_window)
            break
        except:
            pass

def WhereUsed():
    while True:
        try:
            element = driver.find_element(by=By.XPATH, value="//div/a")
            action = ActionChains(driver)
            action.context_click(element).perform()
            break
        except:
            pass
    # Dropdown Clicks
    element = driver.find_element(by=By.LINK_TEXT, value="Where Used")
    element.click()
    while True:
        try:
            ch_window = driver.window_handles[2]
            driver.switch_to.window(ch_window)
            break
        except:
            pass
    xpath_type("//select[3]","ACT",False)
    xpath_click("//select[3]")
    xpath_click("//span[3]")
    tempclip=pyperclip.paste()
    os.chdir(tempdir)
    with open('clipboard.txt','w') as file:
        file.write(tempclip)
    time.sleep(1)
    df = pd.read_csv("clipboard.txt", sep="\t", header=None)
    df.to_excel("OPTemp.xlsx", index=False)

def Modify_View(inp,win):
    while True:
        try:
            element = driver.find_element(by=By.XPATH, value=inp)
            action = ActionChains(driver)
            action.context_click(element).perform()
            break
        except:
            pass
    # Dropdown Clicks
    element = driver.find_element(by=By.LINK_TEXT, value="Structure Management")
    element.click()
    try:
        element = driver.find_element(by=By.LINK_TEXT, value="Modify/View")
        element.click()
    except:
        print(PN, "is having live revision")
        return
    while True:
        try:
            ch_window = driver.window_handles[win]
            driver.switch_to.window(ch_window)
            break
        except:
            pass

def Download():
    xpath_click("//div/a")
    while True:
        try:
            ch_window = driver.window_handles[2]
            driver.switch_to.window(ch_window)
            break
        except:
            pass
    xpath_click("//tr[4]/td[3]/a/b")
    while True:
        try:
            ch_window = driver.window_handles[3]
            driver.switch_to.window(ch_window)
            break
        except:
            pass
    time.sleep(5)

def Browser_Clean():
    while True:
        try:
            ch_window = driver.window_handles[1]
            driver.switch_to.window(ch_window)
            driver.close()
            pass
        except:
            break
    ch_window = driver.window_handles[0]
    driver.switch_to.window(ch_window)












