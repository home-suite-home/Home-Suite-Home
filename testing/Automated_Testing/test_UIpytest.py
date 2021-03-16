# Selenium test for UI 
import pytest 
from selenium import webdriver 
import sys 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep

# Function to get the current cards array 
def find_cards(chrome_driver):
    cards = chrome_driver.find_elements_by_id("fields-card")
    print(len(cards))

    for card in cards:
        print(card)
    return cards

# Function to interact with the cards
def interact_card(chrome_driver, card, sample_card):

    sensorName_field = card.find_element_by_id("field_sensor-name")
    sensorName_field.send_keys(sample_card['name'])
    sleep(2)

    # Select the dropdown 
    chrome_driver.find_element_by_class_name("Select-placeholder").click()
    #sensorType_drop = chrome_driver.find_element_by_xpath(
    #    "//*[contains(text(), 'Sensor Type')]").click()
    sleep(2)

    # Make a new type of sensor 
    chrome_driver.find_element_by_class_name("Select-menu-outer").click()
    newTypeName_field = card.find_element_by_id("field_new-type")
    newTypeName_field.send_keys(sample_card['type'])
    sleep(2)

    '''
    if (sample_card['type'] == 'temperature'):
        chrome_driver.find_element_by_xpath(
            "//input[@aria-activedescendant='react-select-2--option-0']").select()
    sleep(2)
    '''

    IPaddress_field = card.find_element_by_id("field_ip-address")
    IPaddress_field.send_keys(sample_card['IPaddress'])
    sleep(2)

    portNumber_field = card.find_element_by_id("field_port-number")
    portNumber_field.send_keys(sample_card['port'])
    sleep(2)

    URLplug_field = card.find_element_by_id("field_url-plug")
    URLplug_field.send_keys(sample_card['URL_plug'])
    sleep(2)

    # Clicking alert switch and creating a new card 
    card.find_element_by_id("field_alert").click()
    sleep(2)
    card.find_element_by_id("field_create-card-button").click()
    sleep(3)


def test_lambdatest_todo_app():
    chrome_driver = webdriver.Chrome()

    # obtaining connection to the dash server and opening chrome 
    # Note: Dash server must be running in order to obtain connection   
    chrome_driver.get('http://10.0.0.61:8050/')
    chrome_driver.maximize_window()
    sleep(2)

    # Selecting temperature checkbox
    #chrome_driver.find_element_by_xpath("//*[contains(text(), 'Temperature')]").click()
    #sleep(1)
    # Selecting humidity checkbox
    #chrome_driver.find_element_by_xpath("//*[contains(text(), 'Humidity')]").click()
    #sleep(1)
    # Save the selections
    #id_check = "save-checkmarks-button"
    #chrome_driver.find_element_by_id(id_check).click()
    #sleep(8)

    # At this point sensor cards should appear; 
    # click refresh to see them change
    # Note: sensorSim_random must be running in order to see these change 

    chrome_driver.find_element_by_id("new-card-button").click()
    sleep(3)

    # sample fields to populate the new card 
    '''
    sample_sensorName = "Temp_1"
    sample_IPaddress = "localhost"
    sample_portNumber = "8080"
    sample_URLplug = "temperature"
    '''

    sample_data = [
                    {
                        "name": "Temp_1",
                        "type": "temperature",
                        "IPaddress": "localhost",
                        "port": "8080",
                        "URL_plug":"temperature"},
                    {
                        "name":"Humid_1", 
                        "type": "humidity", 
                        "IPaddress": "localhost", 
                        "port": "8080", 
                        "URL_plug": "humidity"},
                    {
                        "name": "Outdoor_1",
                        "type": "light_intensity",
                        "IPaddress": "localhost",
                        "port": "8080",
                        "URL_plug": "temperature"
                    }]
     

    # populating the new sensor fields 
    '''
    cards = chrome_driver.find_elements_by_id("fields-card")
    print(len(cards))

    for card in cards:
        print(card)
    '''
    cards = find_cards(chrome_driver)
    interact_card(chrome_driver, cards[0], sample_data[0])

    card_container = chrome_driver.find_element_by_id("cards-container")

    new_card = card_container.find_elements_by_id("new-card")

    '''
    print(len(new_cards))

    for new_card in new_cards:
        print(new_card)
    '''
    new_card[0].find_element_by_id("new-card-button").click()
    sleep(3)

    # Updating names for humidity sensor card 
    sample_sensorName = "Humid"
    sample_IPaddress = "localhost"
    sample_portNumber = "8080"
    sample_URLplug = "humidity"

    cards = find_cards(chrome_driver)
    interact_card(chrome_driver, cards[0], sample_data[1])

    '''
    sensorName_field = cards[1].find_element_by_id("field_sensor-name")
    sensorName_field.send_keys(sample_sensorName)
    sleep(2)

    IPaddress_field = cards[1].find_element_by_id("field_ip-address")
    IPaddress_field.send_keys(sample_IPaddress)
    sleep(2)

    portNumber_field = cards[1].find_element_by_id("field_port-number")
    portNumber_field.send_keys(sample_portNumber)
    sleep(2)

    URLplug_field = cards[1].find_element_by_id("field_url-plug")
    URLplug_field.send_keys(sample_URLplug)
    sleep(2)

    cards[1].find_element_by_id("field_create-card-button").click()
    sleep(5)
    '''

    # Populating the email field 
    sample_text = "home.suite.home.test.user@gmail.com"
    email_text_field = chrome_driver.find_element_by_id("remote-email")
    email_text_field.send_keys(sample_text)
    sleep(3)

    sleep(42)
    # Sending the email 
    id_send = "button"
    chrome_driver.find_element_by_id(id_send).click()

    # Closing the connection to the server and exiting browser 
    chrome_driver.close()

test_lambdatest_todo_app()
