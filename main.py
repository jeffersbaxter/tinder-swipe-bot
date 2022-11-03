import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")
FACEBOOK_USER = os.environ.get("EMAIL")
FACEBOOK_PASSWORD = os.environ.get("PASSWORD")

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

driver.get("https://tinder.com/")

time.sleep(3)

try:
    login_button = driver.find_element(By.XPATH, '//*[@id="o-2124353878"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a')
except NoSuchElementException:
    print("Could not login")
    driver.quit()
else:
    login_button.click()
    time.sleep(2)
    try:
        login_facebook = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Log in with Facebook']")
    except NoSuchElementException:
        driver.quit()
    else:
        login_facebook.click()
        time.sleep(2)

        base_window = driver.window_handles[0]
        fb_login_window = driver.window_handles[1]
        driver.switch_to.window(fb_login_window)
        # User field
        email = driver.find_element(By.XPATH, '//*[@id="email"]')
        password = driver.find_element(By.XPATH, '//*[@id="pass"]')
        email.send_keys(FACEBOOK_USER)
        password.send_keys(FACEBOOK_PASSWORD)
        password.send_keys(Keys.ENTER)

        driver.switch_to.window(base_window)
        time.sleep(5)
        location = driver.find_element(By.XPATH, '//*[@id="o442232342"]/main/div/div/div/div[3]/button[1]')
        accept_cookies = driver.find_element(By.XPATH, '//*[@id="o-2124353878"]/div/div[2]/div/div/div[1]/div[1]/button')
        location.click()
        accept_cookies.click()
        time.sleep(3)
        notifications_not_interested = driver.find_element(By.XPATH, '//*[@id="o442232342"]/main/div/div/div/div[3]/button[2]')
        notifications_not_interested.click()
        time.sleep(5)
        dark_modal_close = driver.find_element(By.XPATH, '//*[@id="o442232342"]/main/div/div[2]/button')
        dark_modal_close.click()
        time.sleep(3)
        likes = 100
        while likes > 0:
            try:
                like_button = driver.find_element(By.XPATH, '//*[@id="o-2124353878"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[4]/div/div[4]/button')
            except NoSuchElementException:
                time.sleep(2)
                like_button = driver.find_element(By.XPATH, '//*[@id="o-2124353878"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[5]/div/div[4]/button')
            except ElementClickInterceptedException:
                try:
                    match_popup = driver.find_element(By.CSS_SELECTOR, ".itsAMatch a")
                    match_popup.click()
                except NoSuchElementException:
                    time.sleep(2)
                    # consider Add Tinder to your Home Screen modal > Not interested
                    like_button = driver.find_element(By.XPATH,
                                                      '//*[@id="o-2124353878"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[5]/div/div[4]/button')
            finally:
                like_button.click()
            likes -= 1
            time.sleep(3)
        driver.quit()
