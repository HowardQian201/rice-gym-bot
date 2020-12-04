from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from config import keys
import time
from datetime import datetime
from threading import Timer
from webdriver_manager.chrome import ChromeDriverManager


def check_registration_exists():
    for i in range(1, 49, 2):
        num = 50 - i
        if (len(driver1.find_elements_by_xpath(f'//*[@id="mainContent"]/div[2]/div[7]/div[{num}]/div/div/div/button')) > 0):
            return num
            break

def check_sms_passcode():
    for i in range(100):
        num = 100 - i
        if (len(driver2.find_elements_by_xpath(f'//*[@id="messageView"]/ul/li[{num}]/div/div[1]/div/div[1]/div/span')) > 0):
            return num

def time_start(hour_time, minute_time):
    x = datetime.today()
    y = x.replace(day=x.day + 1, hour=hour_time, minute=minute_time, second=1, microsecond=0)
    delta_t = y - x
    secs = delta_t.seconds + 1
    t = Timer(secs, order)
    t.start()

def three_pm_time_start():
    x = datetime.today()
    y = x.replace(day=x.day + 1, hour=15, minute=0, second=1, microsecond=0)
    delta_t = y - x
    secs = delta_t.seconds + 1
    t = Timer(secs, order)
    t.start()

def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        print((endTime - startTime)/1000, 's')
        return result
    return wrapper

@timeme
def order():

    #-----------------fix wait times

    #open rec center website and virtual phone
    #log in to netID
    driver1.get(keys['rec_center_url'])
    driver2.get(keys['virtual_phone'])
    time.sleep(1)
    driver1.find_element_by_xpath('//*[@id="gdpr-cookie-accept"]').click()
    time.sleep(1)
    driver1.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div[7]/div[1]/div/div/a').click()
    time.sleep(1)
    driver1.find_element_by_xpath('//*[@id="divLoginOptions"]/div[2]/div[2]/div/button').click()
    time.sleep(1)
    driver1.find_element_by_xpath('//*[@id="username"]').send_keys(keys['netID'])
    driver1.find_element_by_xpath('//*[@id="password"]').send_keys(keys['netIDpassword'])
    driver1.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/form/div[4]/button').click()
    time.sleep(1)

    #log in to virtual phone
    driver2.find_element_by_xpath('//*[@id="google-login"]').click()
    time.sleep(2)
    driver2.find_element_by_xpath('//*[@id="identifierId"]').send_keys(keys['gmail'])
    driver2.find_element_by_xpath('//*[@id="identifierNext"]/div/button').click()
    time.sleep(4)
    driver2.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(keys['gmailpassword'])
    driver2.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()
    time.sleep(3)

    #send DUO sms code to virtual phone
    actions1 = ActionChains(driver1)
    actions1.move_to_element_with_offset(driver1.find_element_by_tag_name('body'), 0, 0)
    actions1.move_by_offset(293, 408).click().perform()
    time.sleep(5)
    actions2 = ActionChains(driver1)
    actions2.move_to_element_with_offset(driver1.find_element_by_tag_name('body'), 0, 0)
    actions2.move_by_offset(330, 500).click().perform()
    time.sleep(3.5)

    #get sms code
    sms_num = check_sms_passcode()
    print("sms num", sms_num)
    astring = driver2.find_element_by_xpath(f'//*[@id="messageView"]/ul/li[{sms_num}]/div/div[1]/div/div[1]/div/span').text
    sms_passcode = astring.split()[-1]
    print(sms_passcode)

    #enter sms passcode
    actions3 = ActionChains(driver1)
    actions3.move_to_element_with_offset(driver1.find_element_by_tag_name('body'), 0, 0)
    actions3.move_by_offset(280, 350).click().send_keys(sms_passcode).perform()
    actions4 = ActionChains(driver1)
    actions4.move_to_element_with_offset(driver1.find_element_by_tag_name('body'), 0, 0)
    actions4.move_by_offset(280, 411).click().perform()
    time.sleep(3)

    #check gym slot
    register_num = check_registration_exists()
    print("register num", register_num)
    driver1.find_element_by_xpath(f'//*[@id="mainContent"]/div[2]/div[7]/div[{register_num}]/div/div/div/button').click()
    time.sleep(2)

    # signature box
    driver1.find_element_by_xpath('//*[@id="signatureCaptureBox0"]').click()
    time.sleep(1)

    canvas = driver1.find_element_by_xpath('//*[@id="signature-pad"]/div[2]/canvas')
    #draw a weird hook
    drawing = ActionChains(driver1) \
        .click_and_hold(canvas).move_by_offset(0,100) \
        .move_by_offset(0,-50).move_by_offset(60,0) \
        .move_by_offset(0,-50).move_by_offset(0,100).release()
    drawing.perform()

    # save button after signature
    driver1.find_element_by_xpath('//*[@id="btnApplySignature"]').click()

    time.sleep(1)
    # click sign now button
    driver1.find_element_by_xpath('//*[@id="btnSign"]').click()
    # checkout button
    driver1.find_element_by_xpath('//*[@id="checkoutButton"]').click()
    time.sleep(1)
    # second checkout button
    driver1.find_element_by_xpath('//*[@id="CheckoutModal"]/div/div[2]/button[2]').click()




if __name__ == '__main__':
    driver1 = webdriver.Chrome(ChromeDriverManager().install())
    driver2 = webdriver.Chrome(ChromeDriverManager().install())
    order()
    #time_start(14, 45)
    #three_pm_time_start()
