# Selenium test for UI 
import pytest 
from selenium import webdriver 
import sys 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep


def test_lambdatest_todo_app():
    chrome_driver = webdriver.Chrome()

    chrome_driver.get('http://127.0.0.1:8050/')
    chrome_driver.maximize_window()

    # Click a sensor checkbox and save the selection 
    chrome_driver.find_element_by_id("enabled-sensors").click()
    chrome_driver.find_element_by_id("save-checkmarks-button").click()
    sleep(5)
    #chrome_driver.find_element_by_id("li2").click()

    # Populating the email field 
    sample_text = "home.suite.home.test.user@gmail.com"
    email_text_field = chrome_driver.find_element_by_id("remote-email")
    email_text_field.send_keys(sample_text)
    sleep(5)
    chrome_driver.find_element_by_id("button").click()

    chrome_driver.close()

test_lambdatest_todo_app()
