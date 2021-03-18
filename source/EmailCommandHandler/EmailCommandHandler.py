'''
//
//  Date: 02/18/2021
//  FileName: EmailCommandHandler.py
//
//  Engineer: David Crumley
//  Contact: david_crumley@knights.ucf.edu
//
//  Description:
        will read mailbox, and respond to all users commands with appropriate response
'''


import sys
sys.path.append("../EmailComponent") # this path will change if files moved
sys.path.append("../Server_Component") # this path will change if files moved
sys.path.append(".")
from EmailController import EmailController
from CommandResponse import CommandResponse
from Database import Database

class EmailCommandHandler:
    def __init__(self):
        user_emails = Database().getAllUsers()
        self.email_controllers = []
        for user in user_emails:
            self.email_controllers.append(EmailController(user['email']))

    def handle_email_command(self):
        for i in range(len(self.email_controllers)):
            # retrieve valid email from mailbox
            incoming_email = self.email_controllers[i].check_mailbox()

            # create response to user command
            # response will be a tuple with first element being text and
            # second element being html
            if (incoming_email != None):
                text_response, html_response, attachment = CommandResponse(incoming_email).get_response()
                # compose and send the email to user
                subject = "Command Response"
                outgoing_email = self.email_controllers[i].compose_email(subject, text_response, html_response, attachment)
                self.email_controllers[i].send_email(outgoing_email)
