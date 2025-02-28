#!/usr/bin/env python3.9
import json
import os
import time
from logging import debug, error
from random import randint

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from classes.chromedriver import driver
from classes.error import *

# Clear Check
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

start = driver()
driver = driver.driver


with open('./settings.json') as config_file:
    config = json.load(config_file)
stormgainemail = config['stormgain_email']
stormgainpw = config['stormgain_pw']
fromA = config['stormgainsleepMIN']
toB = config['stormgainsleepMAX']

#print("Using Agent: " + useragent)
print("Browser started!")


def stormgainsleeper():
    sleeptime = randint(fromA, toB)
    driver.close()
    print('Miner is Active!\nNext Claim in', sleeptime, 'sec')
    time.sleep(sleeptime)
    start.start()


def shortsleep():
    print('Cooldown!\nClose Browser!')
    driver.close()
    ran = randint(600, 1800)
    print("Sleep:", int(ran), "seconds")
    time.sleep(ran)
    start.start()


def countdownSleep():
    print('countdown')
    countdown = driver.find_element(
        By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div/div[3]/div/div[1]/span[2]').get_attribute('innerHTML')
    if countdown == 'Synchronizing':
        start.countdownSleep()
    print(countdown)
    time_converted = sum(x * int(t)
                         for x, t in zip([3600, 60, 1], countdown.split(":"))) + 30
    print('Going to sleep from countdown time + 30s...!\nClose Browser!')
    driver.close()
    print("Sleep:", countdown, "")
    time.sleep(time_converted)
    start.start()


def claimusdt():
    try:
        driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
    except Exception as e:
        print(e)


def checkusdt():
    try:
        # time.sleep(3)
        print('checking USDT')
        html = driver.find_element(
            By.CSS_SELECTOR, '#region-main > div > div:nth-child(2) > div > div.env > div > div > div:nth-child(2) > div.text-gray-1.text-13.md-text-15.leading-4.md-leading-24.text-center > span:nth-child(1)').get_property("innerHTML")
        usdt = html.replace('≈', '')
        print('You have Mined '+str(usdt)+'$')
        if float(usdt) >= float(10):
            print('More Than 10USDT, Claim it now!')
            start.claimusdt()
    except Exception as e:
        print(e)


def stormgain():
    try:

        driver.get("https://app.stormgain.com/crypto-miner/")  # Check Website
        # time.sleep(randint(3,6))

        try:
            try:
                login = driver.find_element(
                    By.CLASS_NAME, "login-view").is_displayed()  # Check for Login Page
            except NoSuchElementException:
                return False
            pass
            if login:

                # pass
                # commit le login
                # driver.get("https://app.stormgain.com/#modal_login")
                debug('Logging in...')
                # time.sleep(randint(3,6))
                driver.find_element(By.ID, "email").send_keys(stormgainemail)
                debug('Inserting Email...')
                driver.find_element(By.ID, "password").send_keys(stormgainpw)
                debug('Inserting Password...')
                driver.find_element(By.CSS_SELECTOR, ".btn-login").click()
                debug('Clicking Login...')

            try:
                login = driver.find_element(
                    By.CLASS_NAME, "login-view").is_displayed()
            except NoSuchElementException:
                return False
            if login:
                driver.find_element(By.CSS_SELECTOR, ".btn-login").click()
                if driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/form/div[5]"):
                    print(driver.find_element(
                        By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/form/div[3]/div").innerHTML)
                    print('Captcha Detected!')
                    if config['headless_mode'] == True:
                        raise CaptchaError(Exception)
                    else:
                        print('Captcha Detected')
                        WebDriverWait.until_not(driver.find_element(
                            By.CSS_SELECTOR, "#recaptcha-anchor > div.recaptcha-checkbox-checkmark"))
                else:
                    error(driver.find_element(
                        By.CSS_SELECTOR, "#modal > div > div.modal-content > form > div.msg-error-wrapper").innerHTML)
        except NoSuchElementException:
            print('No need to login! Great!')
    finally:
        driver.get('https://app.stormgain.com/crypto-miner/')
        # time.sleep(5)
        checkusdt()
        try:
            time.sleep(5)
            driver.find_element(
                By.CSS_SELECTOR, ".font-medium > .text-17").click()
            time.sleep(randint(3, 6))
            stormgainsleeper()
        except NoSuchElementException:
            print('Currently Mining...')
            try:
                # time.sleep(5)
                countdownSleep()
            except:
                shortsleep()
            if KeyboardInterrupt:
                exit()


stormgain()
driver.start()
