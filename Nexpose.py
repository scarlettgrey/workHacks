from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import getopt
import sys
import pyautogui
import time


confName = ''
AssetsFilePath = ''
Assets = []
Engine = 'T' # T for TBS, B for BRN
Scan_Types = 'N' # N for Normal Scan, S for Night Scan

opts, args = getopt.getopt(sys.argv[1:], "n:a:e:s:h")

def help():
    print("Go Get Some Beer")

for opt, val in opts:
    if opt == '-n':
        confName = val
    elif opt == '-a':
        AssetsFilePath = val
    elif opt == '-e':
        Engine = val
    elif opt == '-s':
        Scan_Types = val
    elif opt == '-h':
        help()
        exit()
    
if AssetsFilePath != '':
    with open(AssetsFilePath, 'r') as f:
        tmp = f.readline().strip('\n')
        Assets.append(tmp)
        while tmp:
            tmp = f.readline().strip('\n')
            Assets.append(tmp)
    Assets = Assets[:-1]

opt = webdriver.ChromeOptions()
opt.add_argument('--ignore-certificate-errors')
opt.add_argument('--ignore-ssl-errors')
opt.add_argument('--start-maximized')

d = webdriver.Chrome('chromedriver.exe', chrome_options=opt)
d.get('https://nexsy.telkomsel.co.id:3780/login.jsp')

userName = d.find_element_by_id('nexposeccusername')
userName.send_keys('tsel_williams')

passWord = d.find_element_by_id('nexposeccpassword')
passWord.send_keys('shoottheduck')

d.find_element_by_id('login_button').click()

time.sleep(1)

d.get('https://nexsy.telkomsel.co.id:3780/scan/config.jsp#/scanconfig/engines')
time.sleep(3)
d.find_element_by_id('scanEngineRadio_14').click()

time.sleep(1)

d.find_element_by_id('tab-about ').click()
time.sleep(1)
Name = d.find_element(By.ID, 'scanConfigName')
Name.send_keys(confName)


d.find_element_by_id('tab-assets ').click()
Asset = d.find_element_by_class_name('input')
for ip in Assets:
    Asset.send_keys(ip + ' ')

d.find_element_by_id('tab-templates ').click()
time.sleep(2)
d.find_element_by_id('scanTemp_full-audit_itsecurity').click()

time.sleep(2)
d.find_element_by_id('tab-assets ').click()
d.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
time.sleep(1)
if Scan_Types == 'N':
    ActionChains(d).click(d.find_element_by_id('btnScanConfigSaveAndRun')).perform()
    time.sleep(1.5)
    ActionChains(d).click(d.find_element_by_xpath('//button[@ng-disabled="modalOptions.enableOkButton === false || modalOptions.saveInProgress"]')).perform()
