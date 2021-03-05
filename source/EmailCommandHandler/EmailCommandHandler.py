'''
//
//  Date: 02/18/2021
//  FileName: EmailCommandHandler.py
//
//  Engineer: David Crumley
//  Contact: david_crumley@knights.ucf.edu
//
//  Description:
        will read mailbox, and respond to user command with appropriate response
'''


import sys
sys.path.append("../../source/EmailComponent") # for testing
sys.path.append("../EmailComponent") # this path will change if files moved
sys.path.append(".")
from EmailController import EmailController
from CommandResponse import CommandResponse

class EmailCommandHandler:
    def __init__(self, user_email, device_email):
        self.user_email = user_email
        self.device_email = device_email
        self.email_controller = EmailController(user_email, device_email)

    def handle_email_command(self):
        # retrieve valid email from mailbox
        incoming_email = self.email_controller.check_mailbox()

        # create response to user command
        # response will be a tuple with first element being text and
        # second element being html
        if (incoming_email != None):
            text_response, html_response, attachment = CommandResponse(incoming_email).get_response()
            # compose and send the email to user
            subject = "Command Response"
            outgoing_email = self.email_controller.compose_email(subject, text_response, html_response, attachment)
            self.email_controller.send_email(outgoing_email)
