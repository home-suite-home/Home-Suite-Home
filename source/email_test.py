import sys
sys.path.append(".")
from Email_Component import Email_Component


confirmation = Email_Component("home.suite.home.test.user@gmail.com")
confirmation.confirmation_email()
