import sys
sys.path.append(".")
from EmailCommandHandler import EmailCommandHandler

user_email = "home.suite.home.test.user@gmail.com"
device_email = "home.suite.home.testing@gmail.com"
command_handler = EmailCommandHandler(user_email, device_email)

while(True):
    command_handler.handle_email_command()
