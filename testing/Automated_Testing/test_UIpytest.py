# Selenium test for UI 
import pytest 
from selenium import webdriver 
import sys 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep

def cancel_interaction(chrome_driver):
    chrome_driver.find_element_by_id("edit_discard-button").click()

def delete_card(chrome_driver):
    chrome_driver.find_element_by_id("edit_delete-button").click()

def edit_cardFields(chrome_driver):
    # Change a sensor's name
    sensorName_field = chrome_driver.find_element_by_id("edit_sensor-name")
    sensorName_field.send_keys(Keys.CONTROL, 'a')
    sensorName_field.send_keys(Keys.DELETE)
    sleep(2)
    sensorName_field.send_keys("humid_3")
    sleep(2)
    # Save the change
    chrome_driver.find_element_by_id("edit_save-card-button").click()

def interact_settingsPage(chrome_driver):
    # Going to the settings page
    chrome_driver.find_element_by_xpath("//*[contains(text(), 'Settings')]").click()
    sleep(2)

    # Entering and submitting an email/password for the raspberry pi
    sample_piEmail = "home.suite.home.test.user@gmail.com"
    sample_piPass = "homeuser"
    pi_email_field = chrome_driver.find_element_by_id("pi-email")
    pi_email_field.send_keys(sample_piEmail)
    sleep(1)
    pi_pass_field = chrome_driver.find_element_by_id("pi-password")
    pi_pass_field.send_keys(sample_piPass)
    sleep(2)
    chrome_driver.find_element_by_id("pi-button").click()
    sleep(2)

    # Adding some test user emails 
    user_email1 = "test@gmail.com"
    user_email2  = "testTwo@hotmail.com"
    user_email3  = "testUser@gmail.com"
    user_email_field = chrome_driver.find_element_by_id("user-email-input")

    # Enter first email 
    user_email_field.send_keys(user_email1)
    sleep(1)
    chrome_driver.find_element_by_id("new-user-button").click()
    sleep(2)
    # Enter second email
    user_email_field.send_keys(user_email2)
    sleep(1)
    chrome_driver.find_element_by_id("new-user-button").click()
    sleep(2)
    # Enter third email
    user_email_field.send_keys(user_email3)
    sleep(1)
    chrome_driver.find_element_by_id("new-user-button").click()
    sleep(2)

    # Showing deletion of user emails
    chrome_driver.find_element_by_class_name("Select-value-icon").click()
    sleep(2)

    # Editing the 'Other Settings'
    # Turn on email notifications
    chrome_driver.find_element_by_id("global-switch").click()
    sleep(2)

    # Minimum cooldown 
    minimum_cooldown = "10"
    cooldown_field = chrome_driver.find_element_by_id("email-rate-limit")
    cooldown_field.send_keys(Keys.CONTROL, 'a')
    cooldown_field.send_keys(Keys.DELETE)
    sleep(2)
    cooldown_field.send_keys(minimum_cooldown)
    sleep(2) 

    # Poll Rate
    sensor_pollRate = "85"
    pollRate_field = chrome_driver.find_element_by_id("poll-rate")
    pollRate_field.send_keys(Keys.CONTROL, 'a')
    pollRate_field.send_keys(Keys.DELETE)
    sleep(2)
    pollRate_field.send_keys(sensor_pollRate)
    sleep(2)

    # Now bring the cooldown value up to 15
    for x in range(5):
        cooldown_field.send_keys(Keys.UP)
        sleep(1)
    sleep(1)

    # Now bring the poll rate value down to 80 
    for x in range(5):
        pollRate_field.send_keys(Keys.DOWN)
        sleep(1)
    sleep(1)

    # Return back to the homepage and exit the function
    chrome_driver.find_element_by_xpath("//*[contains(text(), 'Homepage')]").click()


# Function to get the current new cards array 
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
    chrome_driver.get('http://192.168.1.4:8050/')
    chrome_driver.maximize_window()
    sleep(4)

    # Call the function that handles interacting with the settings page
    interact_settingsPage(chrome_driver)
    sleep(2)

    # At this point sensor cards should appear; 
    # click refresh to see them change
    # Note: sensorSim_random must be running in order to see these change 

    # For sprint 7 we are not instantiating any new cards 
    '''
    chrome_driver.find_element_by_id("new-card-button").click()
    sleep(3)
    '''

    # sample fields to populate the new card 
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
    cards = find_cards(chrome_driver)

    edit_cards = chrome_driver.find_elements_by_xpath("//*[contains(text(), 'Edit Card')]")
    print(len(edit_cards))

    # Cancel interaction with the first card 
    edit_cards[0].click()
    sleep(3)
    cancel_interaction(chrome_driver)
    sleep(2)

    # Edit the field of the second card
    edit_cards[1].click()
    sleep(3)
    edit_cardFields(chrome_driver)
    sleep(2)

    # View the graph of the third card 
    view_graphs = chrome_driver.find_elements_by_xpath("//*[contains(text(), 'View Graph')]")
    view_graphs[2].click()
    sleep(8)
    # Return to the homepage
    chrome_driver.find_element_by_xpath("//*[contains(text(), 'Homepage')]").click()
    sleep(4)

    edit_cards = chrome_driver.find_elements_by_xpath("//*[contains(text(), 'Edit Card')]")
    print(len(edit_cards))

    # Delete the fourth card 
    edit_cards[3].click()
    sleep(3)
    delete_card(chrome_driver)
    sleep(8)

    # Code for making a new card and filling it out
    '''
    interact_card(chrome_driver, cards[0], sample_data[0])

    card_container = chrome_driver.find_element_by_id("cards-container")

    new_card = card_container.find_elements_by_id("new-card")

    new_card[0].find_element_by_id("new-card-button").click()
    sleep(3)

    # Updating names for humidity sensor card 
    cards = find_cards(chrome_driver)
    interact_card(chrome_driver, cards[0], sample_data[1])
    '''

    # Closing the connection to the server and exiting browser 
    chrome_driver.close()

test_lambdatest_todo_app()
