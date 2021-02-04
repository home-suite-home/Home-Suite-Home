'''
an initial version of the confirmation email
that will be sent to users at the completion of setup
- email must be a gmail account

for testing purposes:
    * for testing this code, the email will be sent to the
      following email address:

    - recipient email: home.suite.home.test.user@gmail.com
    - recipient pw:    ********
'''



import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():
    try:
        fileObj = open("password.txt", "r")
    except:
        print("Please add the password.txt file to your machine.")
        return

    sender_email = "home.suite.home.testing@gmail.com"
    reciever_email = "home.suite.home.test.user@gmail.com"
    password = fileObj.read().strip('\n')

    fileObj.close()

    message = MIMEMultipart("alternative")
    message["Subject"] = "Home-Suite-Home Confirmation"
    message["from"] = sender_email
    message["to"] = reciever_email

    text = """\
    Congratulations! You have completed the setup and can
    start monitoring your property using the best open-source
    home sensor suite available. """

    html = """\
    <html>
        <body>
            <p>Congratulations!<br>
                You have completed the setup and can start monitoring
                you're property using <a href="https://github.com/home-suite-home/Home-Suite-Home"> the best open-source home sensor suite available</a>
            </p>
        </body>
    </html>
    """

    # convert to MIME objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # add poth objects to the MIME multipart message
    # the html part will be attempted first
    message.attach(part1)
    message.attach(part2)

    # create secure connection and send the send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, reciever_email, message.as_string()
        )
    print("Email sent.")

main()
