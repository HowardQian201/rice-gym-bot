from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from config import *
import time
from webdriver_manager.chrome import ChromeDriverManager


def check_registration_day_and_time(driver, day, hour):
    for xpath in range(1, 49, 2):
        text = driver.find_element_by_xpath(f'//*[@id="mainContent"]/div[2]/div[7]/div[{xpath}]/div/div/h4').text.split()
        text[0] = text[0].replace(',', '')
        text[4] = text[4][:-3]
        if (text[0] == day and text[4] == hour):
            return xpath
        else:
            return -1

def check_sms_passcode(driver):
    for i in range(100):
        num = 100 - i
        if (len(driver.find_elements_by_xpath(f'//*[@id="messageView"]/ul/li[{num}]/div/div[1]/div/div[1]/div/span')) > 0):
            return num

def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        print((endTime - startTime)/1000, 's')
        return result
    return wrapper


@timeme
def order(day, hour):

    #-----------------fix wait times

    #open rec center website and virtual phone
    driver1 = webdriver.Chrome(ChromeDriverManager().install())
    driver1.get(keys['rec_center_url'])
    time.sleep(1)

    #check if requested time exists
    xpath = check_registration_day_and_time(driver1, day, hour)
    if xpath == -1:
        print("Requested day and time is not available to be registered.")
        exit()

    #open virtual phone
    driver2 = webdriver.Chrome(ChromeDriverManager().install())
    driver2.get(keys['virtual_phone'])
    time.sleep(1)

    #log in to netID
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
    sms_num = check_sms_passcode(driver2)
    print("sms num", sms_num)
    astring = driver2.find_element_by_xpath(f'//*[@id="messageView"]/ul/li[{sms_num}]/div/div[1]/div/div[1]/div/span').text
    sms_passcode = astring.split()[-1]
    print(sms_passcode)
    driver2.quit()

    #enter sms passcode
    actions3 = ActionChains(driver1)
    actions3.move_to_element_with_offset(driver1.find_element_by_tag_name('body'), 0, 0)
    actions3.move_by_offset(280, 350).click().send_keys(sms_passcode).perform()
    actions4 = ActionChains(driver1)
    actions4.move_to_element_with_offset(driver1.find_element_by_tag_name('body'), 0, 0)
    actions4.move_by_offset(280, 411).click().perform()
    time.sleep(3)

    #click gym slot
    print('Registration xpath num', xpath)
    driver1.find_element_by_xpath(f'//*[@id="mainContent"]/div[2]/div[7]/div[{xpath}]/div/div/div/button').click()
    time.sleep(2)

    #signature box
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
    print("Only timeslots 48 hours in advance are available for registration.")
    user_input = input('Please enter the day and hour of the slot you want. \nFor Friday 9:45 AM, enter "Friday 9". \nFor Tuesday 2:45 PM, enter "Tuesday 2". \n').split()
    if len(user_input) == 2 and user_input[0] in valid_days and user_input[1] in valid_hours:
        order(user_input[0], user_input[1])
    else:
        print("The input does not match the format.")

