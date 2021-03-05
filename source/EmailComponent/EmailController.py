'''

  Date: 02/018/2021
  FileName: EmailController.py

  Engineer: David Crumley
  Contact: david_crumley@knights.ucf.edu

  Description:

    Provides an API for sending and recieving email_test

    Functions provided by EmailController API:

        compose_email()
        send_email()
        check_mailbox()

'''
import sys
sys.path.append(".")

#  device email => "home.suite.home.testing@gmail.com"
class EmailController:

    # defualt parameters used for automated testing
    def __init__(self, user_email, device_email):
        self.user_email = user_email
        self.device_email = device_email
        # attempting to read password for device email
        try:
            fileObj = open("password.txt", "r")
        except:
            print("Please add the password.txt file to your machine.")
            return

        self.password = fileObj.read().strip('\n')

    def compose_email(self, subject, body_text, body_html, attachments = None):
        # necessary libraries to construct email
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.image import MIMEImage

        # create the email message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["from"] = self.device_email
        message["to"] = self.user_email

        text = body_text
        html = body_html


        # convert to MIME objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # add poth objects to the MIME multipart message
        # the html part will be attempted first
        message.attach(part1)
        message.attach(part2)
        # add attachments
        if attachments:
            fp = open(attachments, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            message.attach(img)

        print("email composed")
        return message.as_string()

    def send_email(self, message):
        #necessary libraries to send email
        import smtplib, ssl
        # create secure connection and send the send the email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.device_email, self.password)
            server.sendmail(
                self.device_email, self.user_email, message
            )
        print("Email sent.")

    def check_mailbox(self):
    # email validation and inbox cleaning handled here
        import imaplib
        import email
        from email.header import decode_header

        # create IMAP4 class with SSL
        imap = imaplib.IMAP4_SSL("imap.gmail.com")

        # login
        imap.login(self.device_email, self.password)

        # search for email from our user
        status, num_messages = imap.select("INBOX")
        type, messages = imap.search(None, 'FROM', self.user_email)

        # convert messages to a simple list of ID's
        messages = messages[0].split()

        # return null if no emails
        if len(messages) == 0:
            return None

        # fetch the newest email from user => last ID in the list
        type, msg = imap.fetch(messages[-1], '(RFC822)')
        #decode message
        for response in msg:
            if isinstance(response, tuple):
                # parse bytes into message object
                msg = email.message_from_bytes(response[1])
                # decode the subject
                subject, encoding = decode_header(msg["subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)

                print("subject:", subject)

                # get the body out (only accepting multipart and plain text RN)
                if msg.is_multipart():
                    # just want the plain text
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode()
                            print(body)
                #plain text
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)

        # delete the email from the inbox
        imap.store(messages[-1], "+FLAGS", "\\Deleted")

        # end the smtp session
        imap.close()
        imap.logout()

        print("checked the mailbox")
        # remove whitespace including /n and /r
        return str(body).strip()
