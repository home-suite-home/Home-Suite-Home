'''
will output appropriate response based on incoming command

will handle accessing the database for sensor data
'''


class CommandResponse:
    def __init__ (self, command):
        self.command = command

    def get_response(self):
        if self.command == "help":
            text_response = "dummy help message"
            html_response = """\
            <html>
                <body>
                    <p>dummy help message<br>
                        <a href="https://github.com/home-suite-home/Home-Suite-Home"> heres a link to the github, figure it out</a>
                    </p>
                </body>
            </html>
            """
            response = (text_response, html_response)
            return response

        else:
            text_response = "dummy help message"
            html_response = """\
            <html>
                <body>
                    <p>dummy help message<br>
                        <a href="https://github.com/home-suite-home/Home-Suite-Home"> heres a link to the github, figure it out</a>
                    </p>
                </body>
            </html>
            """
            response = (text_response, html_response)
            return response
