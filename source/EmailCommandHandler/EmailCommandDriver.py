'''
//  Date: 02/18/2021
//  FileName: CommandHandlerTest.py
//
//  Engineer: David Crumley
//  Contact: david_crumley@knights.ucf.edu
//
//  Description:
        simple script to run the EmailCommandHandler.py module

    Directions:
        1) run this file using the command: python CommandHandlerTest.py
                - you will need to have a file named password.txt in the same folder
        2) send an email to the address: home.suite.home.testing@gmail.com

        3) check your inbox for a reply message, there should be one
'''

import sys
sys.path.append('.')
sys.path.append('../Server_Component')
sys.path.append('..')
import time
from EmailCommandHandler import EmailCommandHandler

command_handler = EmailCommandHandler()

POLL_RATE = 60

while(True):
    command_handler.handle_email_command()
    time.sleep(POLL_RATE)