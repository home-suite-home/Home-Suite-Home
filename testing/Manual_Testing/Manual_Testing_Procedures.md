This file contains instructions for executing manual testing 

# CommandHandlerTest.py 
## Description
Verify *EmailCommandHandler.py* can properly respond to an email sent by a specified user
## Test Tools and Dependencies
The following will be needed for this test:
* Linux Command Line Terminal
* Python standard libraries

* clone the repository on to the local machine: this will ensure all necessary files are found

## Test Cases
### Functional Case
**Test Status** *PASS*</br>
#### Test Procedures
| No. | Steps to Reproduce | Expected Behavior |
| --- | --- | --- |
| 1 | In the linux command line terminal, from the repo's main directory, move to the manual testing directory| ![cd](/artifacts/assets/move_to_testing.PNG) |
| 2 | In the linux terminal, enter the command $python CommandHandlerTest.py | ![prompt](/artifacts/assets/CommandHandlerCommand.PNG) |
| 3 | When prompted, enter the email address that will be used to communicate with the program | ![prompt](/artifacts/assets/enter_email.PNG) |
| 4 | Using an email application, send an email to 'home.suite.home.testing@gmail.com' | ![test_request](/artifacts/assets/test_request.PNG) |

#### Test Results
| No. | Expected Results | Actual Results |
| --- | --- | --- |
| 1 | The terminal will reflect the operations being handled by the running program | ![terminal_response](/artifacts/assets/terminal_response.PNG) |
| 2 | An email message will be recieved by 'home.suite.home.testing@gmail.com' | ![email_response](/artifacts/assets/email_response.PNG) |

### Negative Case
**Test Status** *PASS*</br>
#### Test Procedures
| No. | Steps to Reproduce | Expected Behavior |
| --- | --- | --- |
| 1 | In the linux command line terminal, move to the directory (/testing/Manual_Testing) | ![cd](/artifacts/assets/move_to_testing.PNG) |
| 2 | In the linux terminal, enter the command $python CommandHandlerTest.py | ![prompt](/artifacts/assets/CommandHandlerCommand.PNG) |
| 3 | When prompted, enter an email address different than the one that will be used to communicate with the system | ![prompt](/artifacts/assets/non_user.PNG) |
| 4 | Using an email application, send an email to 'home.suite.home.testing@gmail.com' from the email used in the Functional Test| ![test_request](/artifacts/assets/test_request.PNG) |

#### Test Results
| No. | Expected Results | Actual Results |
| --- | --- | --- |
| 1 | The terminal will not show anything | ![terminal_response](/artifacts/assets/no_response.PNG) |
| 2 | An email message will not be recieved by 'home.suite.home.testing@gmail.com' | ![email_response](/artifacts/assets/empty_email.PNG) |

# Sensors.py
## Description
Verify *Sensors.py* can properly access sensor data from a web server, convert units and display the results correctly.
## Test Tools and Dependencies 
For this test, we are begining with the following tools installed:
* Linux Text Editor (Or Similar Code Editing Tool)
* Linux Command Line 

We will also need the source code we are testing as well as our test script:
* [Sensors.py](/source/HTTP_Component/Sensors.py)
* [sensorSim_constant.py](/testing/Manual_Testing/sensorSim_constant.py)

Note: For simplicity, move both source files into a test directory on the local machine.

## Test Cases
### Functional Case
**Test Status:** *PASS*

**Test Data:**
We will use *25.00* for our degrees Celsius and *50.00* percent for our relative humidity. These numbers are typical values for indoor room conditions.
| No. | Steps to Reproduce | Expected Behavior |
| --- | --- | --- |
| 1 | Open the directory containing both *Sensors.py* and *sensorSim_constant.py* | A folder containing both source files should appear on the screen |
| 2 | Right click in the directory window and select the *Open in Terminal* option | A terminal window will appear with the correct directory showing to the right of the users name |
| 3 | Right click in the directory window for a second time and again select the *Open in Terminal* option | A second terminal window should appear again showing the correct directory name to the right of the users name |
| 4 | In the first terminal window type *python3 sensorSim_constant.py* and press the return key | The terminal window will display the message *Server started ht<span>tp://</span>localhost:8080* |
| 5 | In the second terminal window type *python3 Sensors.py* and press return | The following output will be observed in the terminal: ![Sensor.py Nominal Output](/artifacts/assets/sensor_py_output.PNG)|
| 6 | Compare the temperature in degrees Fahrenheit from the terminal output from *Sensors.py* shown in step 5 to a known conversion from 25.00 degrees Celsius to Fahrenheit [WolframAlpha Temperature Conversion](https://www.wolframalpha.com/input/?i=25.00+Celsius+to+Fahrenheit) | The *Sensor.py* terminal output for degrees Fahrenheit will match the WolframAlpha reference value |
| 7 | Verify the relative humidity displayed in the terminal output from *Sensors.py* matches the test data of 50.0 | The relative humidity displayed in the terminal output for *Sensors.py* will match the test data value of 50.0 |
| 8 | Verify the dew point displayed in the *Sensors.py* terminal output matches the first three significant digits from right to left of the [reference value 56.9](https://www.calculator.net/dew-point-calculator.html?airtemperature=25.0&airtemperatureunit=celsius&humidity=50&dewpoint=&dewpointunit=fahrenheit&x=87&y=22) | The dew point from the terminal output of *Sensors.py* will match the reference value |

### Negative Case
**Test Status:** *PASS*

**Test Data:**
No test data needed.
| No. | Steps to Reproduce | Expected Behaviour |
| --- | --- | --- |
| 1 | Open the directory containing both *Sensors.py* and *sensorSim_constant.py* | A folder containing both source files should appear on the screen |
| 2 | Right click the *Sensor.py* file and click on the *Open With Text Editor* option | A context menu will appear when the *Sensors.py* file is right clicked and when the *Open With Text Editor* option is left clicked from that menu, a text editor displaying the *Sensor.py* source code. |
| 3 | Scroll down to line 98 and change the word in parenthesis from *temperature* to *fail* | The word *temperature* is replaced with the word *fail* |
| 4 | Scroll down to line 103 and change the word in parenthesis from *temperature* to *fail* | The word *temperature* is replaced with the word *fail* |
| 5 | Left click save in the upper right corner of the text editor to save the modified version of *Sensors.py* | The modified *Sensor.py* file will be saved |
| 6 | Close the text editor | The text editor window will disappear |
| 7 | Open the directory containing both *Sensors.py* and *sensorSim_constant.py* | A folder containing both source files should appear on the screen |
| 8 | Right click in the directory window and select the *Open in Terminal* option | A terminal window will appear with the correct directory showing to the right of the users name |
| 9 | Right click in the directory window for a second time and again select the *Open in Terminal* option | A second terminal window should appear again showing the correct directory name to the right of the users name |
| 10 | In the first terminal window type *python3 sensorSim_constant.py* and press the return key | The terminal window will display the message *Server started ht<span>tp://</span>localhost:8080* |
| 11 | In the second terminal window type *python3 Sensors.py* and press return | The following output will be observed in the terminal: ![Sensor.py Nominal Output](/artifacts/assets/sensor_output_fail.PNG) |
| 12 | Observe the error from step 11 causes a crash resulting from incorrectly formatted data. | This error is expected behavior and is slated to be revised in future versions. |


# posttester.js
## Description
This test script sends a JSON document of mock sensor data to the local webserver from the posthandler.js script. The purpose of this script is to confirm that the webserver recieves data in a similar format to the sensor data, and will successfully push it to the database for later viewing.

## Testing Requirements and Dependencies
To set up a test environment in which to run the code, the following tools are required:

* Bash shell(or a similar Unix terminal emulator)
* [MongoDB Community Server](https://www.mongodb.com/try/download/community)
* [Node.js](https://nodejs.org/en/)

Before running any of the programs listed here, it is recomended to follow the procedures for [setting up the server process for MongoDB](https://docs.mongodb.com/manual/administration/install-on-linux/), followed by [the installation process for Node.js](https://nodejs.org/en/download/). After which, you'll want to run the following command inside the project folder to install the dependencies for Node.js to interact with MongoDB...

```shell
user@machine:~$ npm init -y; npm install mongodb
```
## Test Procedures

| No. | Steps to Reproduce | Expected Behavior |
| --- | --- | --- |
|  1  | Open the terminal, and procede to project directory| The project file should contain both the *posthandler.js* and *posttester.js* files|
|  2  | run the posthandler file using the *node posthandler.js* command| The following output should be displayed in the terminal![posthandler](/artifacts/assets/posthandler_out1.png)|
|  3  | Open another terminal window, and run the posttester.js script | The posttester.js script should return a starus code of 200, signifying a successful reply from the posthandler|
|  4  | Procede to the terminal window running the posthandler| The posthandler should disply the following result:![posthandler](/artifacts/assets/posthandler_out2.png)|
|  5  | Open another terminal window and run the *mongo* command to open the mongo shell| The mongo shell opens|
|  6  | Enter the *use sensorsdb* command followed by the *db.sensors.find({})* command to select the database for the sensors, and query the *sensors* collection for all of its members| The database outputs the sensor record inserted by the posttester.js script. ![mongo_Out](/artifacts/assets/mongo_Out.png)|

# Database_test.py
## Description
This test script works to interact with the MongoDB database that will house the records for all of our sensors. The purpose of this script is to prove that we have connection to the database and can make edits to it without going through the database's GUI. 

## Testing Requirements and Dependencies
To set up a test environment in which to run the code, the following tools are required:

* Bash shell(or a similar Unix terminal emulator)
* [MongoDB Community Server](https://www.mongodb.com/try/download/community)
* Database.py

Before running any of the programs listed here, it is recomended to follow the procedures for [setting up the server process for MongoDB](https://docs.mongodb.com/manual/administration/install-community/) on your operating system. If you want access to a GUI for the database, it is recommended that you choose to install on either macOS or Windows. Ensure that *Database_test.py* and *Databse.py* are in the same directory on your machine before running. 

## Test Procedures

| No. | Steps to Reproduce | Expected Behavior |
| --- | --- | --- |
|  1  | Open the file *Database_test.py* on a text editor of your choice, and uncomment the line db.Clear() if it is not already | The line will light up to indicate that it will be compiled when ran |
|  2  | Open the terminal and procede to the directory containing the required files | The directory should contain both files required for testing when inputting the commands *ls* or *dir* on the command line |
|  3  | Run the *Database_test.py* script | Upon opening the mongoDB GUI (if running on macOS or Windows) you should see an empty databse called *sensorsdb* ![empty](artifacts/assets/empty_sensorsdb.PNG) |
|  4  | Return to the *Database_test.py* file and now comment out the line db.Clear() | The posthandler should disply the following result:![posthandler](/artifacts/assets/posthandler_out2.png)|
|  5  | Open another terminal window and run the *mongo* command to open the mongo shell| The mongo shell opens|
|  6  | Enter the *use sensorsdb* command followed by the *db.sensors.find({})* command to select the database for the sensors, and query the *sensors* collection for all of its members| The database outputs the sensor record inserted by the posttester.js script. ![mongo_Out](/artifacts/assets/mongo_Out.png)|



 
