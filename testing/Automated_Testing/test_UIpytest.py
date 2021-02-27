# Selenium test for UI 
import pytest 
from selenium import webdriver 
import sys 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep


def test_lambdatest_todo_app():
    chrome_driver = webdriver.Chrome()

    # obtaining connection to the dash server and opening chrome 
    # Note: Dash server must be running in order to obtain connection   
    chrome_driver.get('http://127.0.0.1:8050/')
    chrome_driver.maximize_window()
    sleep(2)

    # Selecting temperature checkbox
    chrome_driver.find_element_by_xpath("//*[contains(text(), 'Temperature')]").click()
    sleep(1)
    # Selecting humidity checkbox
    chrome_driver.find_element_by_xpath("//*[contains(text(), 'Humidity')]").click()
    sleep(1)
    # Save the selections
    id_check = "save-checkmarks-button"
    chrome_driver.find_element_by_id(id_check).click()
    sleep(8)

    # At this point sensor cards should appear; 
    # click refresh to see them change
    # Note: sensorSim_random must be running in order to see these change 

    buttons = chrome_driver.find_elements_by_css_selector("button")
    print(len(buttons))
   
    # Refresh the temperature sensor card
    # If only one card 
  
    if (len(buttons) > 2):
        print("ATTEMPTING REFRESH - temp\n")
        buttons[2].click()
    sleep(4)

    # Refresh the humidity sensor card
    # Two cards
    
    if (len(buttons) > 3):
       print("ATTEMPTING REFRESH - humid\n")
       buttons[3].click()
    sleep(4)

    # Populating the email field 
    sample_text = "home.suite.home.test.user@gmail.com"
    email_text_field = chrome_driver.find_element_by_id("remote-email")
    email_text_field.send_keys(sample_text)
    sleep(3)

    # Sending the email 
    id_send = "button"
    chrome_driver.find_element_by_id(id_send).click()

    # Closing the connection to the server and exiting browser 
    chrome_driver.close()

test_lambdatest_todo_app()
