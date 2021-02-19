'''
  Date: 02/19/2021
  FileName: test_pytest.py
  
  Engineer: Andres Graterol
  Contact: graterol.andres0@knights.ucf.edu
  Description: 
    Provides automated unit tests for 
    the following functions in EmailController.py:
        compose_email()
        check_mailbox()
'''

# Automated Testing for EmailController.py
from pytest import ExitCode
from EmailController import *

def test_compose_email():
    EmailController.device_email = "home.suite.home.testing@gmail.com"
    EmailController.user_email = "home.suite.home.test.user@gmail.com"
    text_response = "Test"
    html_response = """\
            <html>
                <body>
                    <p>dummy help message<br>
                        <a href="https://github.com/home-suite-home/Home-Suite-Home"> Best POOS Group</a>
                    </p>
                </body>
            </html>
            """
    assert isinstance(EmailController.compose_email(EmailController, "Subject", text_response, html_response), str)

def test_empty_check_mailbox():
    EmailController.device_email = "home.suite.home.testing@gmail.com"
    EmailController.user_email = "home.suite.home.test.user@gmail.com"
    #attempting to read password for device email
    try:
        fileObj = open("password.txt", "r")
    except:
        print("Please add the password.txt file to your machine.")
        return

    EmailController.password = fileObj.read().strip('\n')
    assert EmailController.check_mailbox(EmailController) == None

def test_occupied_check_mailbox(): 
    EmailController.device_email = "home.suite.home.testing@gmail.com"
    EmailController.user_email = "home.suite.home.test.user@gmail.com"
    #attempting to read password for device email
    try:
        fileObj = open("password.txt", "r")
    except:
        print("Please add the password.txt file to your machine.")
        return

    EmailController.password = fileObj.read().strip('\n')
    assert not isinstance(EmailController.check_mailbox(EmailController),str)
