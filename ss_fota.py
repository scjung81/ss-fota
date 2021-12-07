# Chrome version : Chrome	73.0.3683.86 (공식 빌드) (64비트) (cohort: Stable)
# Chrome WebDriver는 Chrome version 이 변경되면 아래 url 에서 변경 필요함.
# Chrome WebDriver : https://sites.google.com/a/chromium.org/chromedriver/downloads
# Chrome version 확인 방법 : chrome 에서 chrome://version/ 로 연결

from time import sleep
import shutil
import os
import sys
from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.chrome import webdriver as chrome_webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException

import pandas as pd

from sendMail import *
sendMail(title="ss_fota started ", text="")

isTest = False

now = datetime.now()
dt = datetime.today().strftime("%Y%m%d_%H%M")

tmpdir = os.path.join(os.getcwd(), "tmp")

#다운 로드 받은 최근 파일일 이름을 변경
def change_download_file_name(str, extension="xlsx"):
    filepath = tmpdir
    filename = max([filepath +"/"+ f for f in os.listdir(filepath)], key=os.path.getctime)
    print(filename)

    if not os.path.exists(os.path.join(os.getcwd(), "data", dt)):
        os.makedirs(os.path.join(os.getcwd(), "data", dt))

    shutil.move(filename, os.path.join(os.getcwd(), "data", dt, str + "_" + dt + "."+extension))
    print(os.path.join(os.getcwd(), "data", dt,  str + "."+extension))
    print("=========")

def downloads_done():
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    for i in os.listdir(tmpdir):
        if ".crdownload" in i:
            sleep(0.5)
            downloads_done()


class DriverBuilder():
    def get_driver(self, download_location=None, headless=False):

        driver = self._get_chrome_driver(download_location, headless)
        driver.implicitly_wait(5) ## 암묵적으로 웹 자원을 (최대) 3초 기다리기

        # driver.set_window_size(1400, 700)

        return driver

    def _get_chrome_driver(self, download_location, headless):
        chrome_options = chrome_webdriver.Options()
        if download_location:
            # prefs = {'download.default_directory': download_location,
            #          'download.prompt_for_download': False,
            #          'download.directory_upgrade': True,
            #          'safebrowsing.enabled': False,
            #          'safebrowsing.disable_download_protection': True}

            prefs =  { 'download.default_directory': download_location,
                        'download.prompt_for_download': False,
                        'download.directory_upgrade': True,
            }

            chrome_options.add_experimental_option('prefs', prefs)


        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('log-level=0')

        # chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        # chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument("disable-gpu")
        # chrome_options.add_argument("lang=ko_KR") # 한국어!

        # dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = "c:/"
        driver_path = os.path.join(dir_path, "drivers/chromedriver")

        if sys.platform.startswith("win"):
            driver_path += ".exe"

        driver = Chrome(executable_path=driver_path, options=chrome_options)

        if headless:
            self.enable_download_in_headless_chrome(driver, download_location)

        return driver

    def enable_download_in_headless_chrome(self, driver, download_dir):
        """
        there is currently a "feature" in chrome where
        headless does not allow file download: https://bugs.chromium.org/p/chromium/issues/detail?id=696481
        This method is a hacky work-around until the official chromedriver support for this.
        Requires chrome version 62.0.3196.0 or above.
        """

        # add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)
        print("response from browser:")
        for key in command_result:
            print("result:" + key + ":" + str(command_result[key]))


from connection_info import get_connection_info
#ID/PW
ss_fota_id = get_connection_info("ss_fota_id")
ss_fota_pw = get_connection_info("ss_fota_pw")  #<-- 3개월단위 업데이트 필요

#headless_raw = "FALSE"   #for test
#headless_raw = "TRUE"   #headless 모드, 자동화시 필요

host = get_connection_info("ss_fota_host")

if (isTest == True) :
    headless = False
else :
    headless = True
#headless = False
print("headless = " + str(headless))

######################################################################################

#크롤링 xpath찾아서 버튼 클릭
#이전 명령이 완료되지 않으면 대기하며 클릭
def find_xpath_click(driver, xpath, decribe="", wait=30):
    print(decribe + ":" + xpath)
    for i in range(wait):
        try:
            driver.find_element_by_xpath(xpath).click()
            break
        except ElementClickInterceptedException as e:
            print('retry in 1s.(' + str(i) + ")")
            sleep(1)
    else:
        raise Exception


def login_ss_fota():
    ## Login
    db = DriverBuilder()
    driver = db.get_driver(tmpdir, headless)
    driver.get(host)
    driver.find_element_by_name('emailID').send_keys(ss_fota_id) ## 값 입력
    driver.find_element_by_name('password').send_keys(ss_fota_pw)
    find_xpath_click(driver, '/html/body/form/div/div/div/div[2]/div[1]/div[1]/div[2]/button', "로그인 버튼")
    return driver

try :
    driver = login_ss_fota()
except Exception as ex:
    print(ex)
    print("Please Check chromedriver version..")
    exit(-1)


try :
#     # 로그인 여부 확인
    find_xpath_click(driver, '/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/a', "Last Access Information 창 종료") #Last Access Information 창 종료
except Exception as ex:
    print(ex)
#     sendSMS(ex.msg)
#     exit(-1)



#find_xpath_click(driver, '//html/body/div[1]/div[2]/div[1]/div/div[2]/ul/li[5]/a/span[1]/img', "Realtime")
find_xpath_click(driver, '/html/body/div[1]/div[2]/div[1]/div/div[2]/ul/li[2]/a/span[1]/img', "Realtime")
#find_xpath_click(driver, '/html/body/div[2]/div[1]/div[1]/div/ul/li[4]/ul/li[2]/ul/li[1]/a/div', "Version Count on Market")
find_xpath_click(driver, '/html/body/div[2]/div[1]/div[1]/div/ul/li[2]/ul/li[2]/ul/li[1]/a/div', "Version Count on Market")

find_xpath_click(driver, "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/form/div[1]/div/div/div[2]/div[4]/div[2]/div/span[2]", "CC ALL 체크")
find_xpath_click(driver, "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/form/div[1]/div/div/div[2]/div[4]/div[3]/div/span[2]", "Model ALL 체크")
find_xpath_click(driver, '/html/body/div[2]/div[1]/div[2]/div[1]/div/div[2]/form/div/div[2]/p/a', "Search")
find_xpath_click(driver, '/html/body/div[2]/div[1]/div[2]/div[1]/div/div[2]/form/div/div[3]/div/div[2]/p/a', "XLS Report", wait=150)

# 다운로드 파일 이름 변경
while(1):
    sleep(1)
    downloads_done()
    try:
        change_download_file_name("ss_fota_real_time")
    except Exception as ex:
        print("waiting..")
        continue
    break

################################
# import datetime as dt
from datetime import datetime, timedelta
from dateutil.parser import parse
import math

def getCurrentDate():
    dt = datetime.now()
    return dt.strftime("%Y%m%d")

def getshiftday(day1, dayshift):
    date = parse(day1) + timedelta(days = dayshift)
    return date.strftime("%Y%m%d")

def diff_month(d1, d2):
    d1 = parse(d1)
    d2 = parse(d2)
    return (d1.year - d2.year) * 12 + d1.month - d2.month

# 6일 전(서버 default 설정 값)에서 90일 전으로 가려면 몇달을 뒤로 갈건지 리턴
def getdeltamonth_6to90():
    day1 = getshiftday(getCurrentDate(), -8)
    day2 = getshiftday(getCurrentDate(), -89)
    month_cnt = diff_month(day1, day2)
    print('getdeltamonth_6to90()  d1:{}, d2:{}, month_cnt:{}'.format(day1,day2,month_cnt))
    return month_cnt

# 켈린더에서 x,y 좌표 반환
def getcelenderxy(day):
    # day = datetime.now()
    # day = dt.datetime.strptime("20200131", '%Y%m%d')

    wd = (day.weekday()%7)
    firstwd = (datetime.strptime("{0:>04d}{1:>02d}01".format(day.year,day.month), '%Y%m%d').weekday())%7 #해당월 1일의 요일
    weekindex = math.ceil((day.day + firstwd) / 7)
    print ("getcelenderxy() day:{}, wd:{}, day.day:{}, weekindex:{}, firstwd:{}".format(day, wd, day.day, weekindex, firstwd))
    return wd+2, weekindex

# device_by_version
find_xpath_click(driver, '/html/body/div[2]/div[1]/div[1]/div/ul/li[1]/h2/a', "DEVICE", wait=70)
find_xpath_click(driver, '/html/body/div[2]/div[1]/div[1]/div/ul/li[1]/ul/li/ul/li[1]/a/div', " By version")

#find_xpath_click(driver, "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/form/div[1]/div/div/div[2]/div[4]/div[2]/div/span[2]/input", "CC ALL 체크")
find_xpath_click(driver, '/html/body/div[2]/div[1]/div[2]/div[1]/div/div[2]/form/div/div[1]/div/div[2]/div[4]/div[2]/dd/button/span[2]', "CC입력")
find_xpath_click(driver, '/html/body/div[8]/ul/li[1]/label/span', "SKC 체크")
find_xpath_click(driver, "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/form/div[1]/div/div/div[2]/div[4]/div[3]/div/span[2]/input", "Model ALL 체크")

#90일 전으로 설정
#find_xpath_click(driver, "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/form/div[1]/div/div/div[1]/div[2]/div[1]/img", "Date Range_start")
find_xpath_click(driver, "/html/body/div[2]/div[1]/div[2]/div[1]/div/div[2]/form/div/div[1]/div/div[1]/div[2]/div[1]/img", "Date Range_start")

for j in range(0, getdeltamonth_6to90()):
    #find_xpath_click(driver, "/html/body/div[24]/div/a[1]/span", "Previous month")
    find_xpath_click(driver, "/html/body/div[27]/div/a[1]/span", "Previous month")

x,y = getcelenderxy(parse(getshiftday(getCurrentDate(), -89)))
#find_xpath_click(driver, "/html/body/div[24]/table/tbody/tr[{0}]/td[{1}]/a".format(y,x), "Select Day")
find_xpath_click(driver, "/html/body/div[27]/table/tbody/tr[{0}]/td[{1}]/a".format(y,x), "Select Day")

#find_xpath_click(driver, "/html/body/div[2]/div[1]/div[2]/div[1]/div/div[2]/form/div/div[1]/div/div[1]/div[1]/div[2]/ul/li[1]/a".format(y,x), "Select Day")
#find_xpath_click(driver, "/html/body/div[2]/div[1]/div[2]/div[1]/div/div[2]/form/div/div[1]/div/div[1]/div[1]/div[2]/ul/li[1]/a", "Click Day")

find_xpath_click(driver, '/html/body/div[2]/div[1]/div[2]/div[1]/div/div[2]/form/div/div[2]/p/a', "Search")

find_xpath_click(driver, '/html/body/div[2]/div[1]/div[2]/div[1]/div/div[2]/form/div/div[3]/div/div[2]/p/a', "XLS Report", wait=150)

# 다운로드 파일 이름 변경
while(1):
    sleep(1)
    downloads_done()
    try:
        change_download_file_name("ss_fota_device_by_version")
    except Exception as ex:
        print("waiting..")
        continue
    break

driver.quit()
print("Complete Downloading!!")
#
from make_db_data_ss_fota import StartMakeDb_current
StartMakeDb_current()

from make_db_data_ss_fota_device_by_version import StartMaeDb_last90days
StartMaeDb_last90days()

# Send Mail
recevier_list = ["sukchan.jung@sktelecom.com", 'ywhan@sktelecom.com', 'jaehyun.ryu@sktelecom.com',
                 'jbmoon@sktelecom.com', 'jtchoi20@sktelecom.com', 'chris.mclee@sktelecom.com',
                 'jiyoun_choi@sktelecom.com', 'byungjo.min@sktelecom.com',
                 'jongkeunjung@sktelecom.com', "9164c98a.o365skt.onmicrosoft.com@apac.teams.ms"]
recevier_list_test = ["58fc60be.o365skt.onmicrosoft.com@apac.teams.ms", "sukchan.jung@sktelecom.com"]
custom_model = [['SM-G970N', 'SM-G973N', 'SM-G975N', 'SM-G960N', 'SM-G965N', 'SM-G950N', 'SM-G955N', 'SM-N960N', 'SM-N950N']]


from ss_fota_send_email import start_send_report_email
from ss_fota_send_email_custom import start_send_report_email_custom
from ftpupload_fota import start_upload

if (isTest == True) :
    start_send_report_email(recevier_list_test)
    start_send_report_email_custom(custom_model, recevier_list_test)
else :
    start_send_report_email(recevier_list)
    start_send_report_email_custom(custom_model, recevier_list)
    file_list = start_upload()
    sendMail(title="ss_fota end ", text="")

