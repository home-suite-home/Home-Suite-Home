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
**Test Status** *PASS*
**Test Procedures**
1. In the linux command line terminal, move to the directory (/testing/Manual_Testing)
2. In the linux terminal, enter the command $python CommandHandlerTest.py
3. When prompted, enter the email address that will be used to communicate with the program
4. Using an email application, send an email to 'home.suite.home.testing@gmail.com'
**Test Results**
1. The terminal will reflect the operations being handled by the running program
2. An email message will be recieved by 'home.suite.home.testing@gmail.com'

### NEgative Case
**Test Status** *PASS*
**Test Procedures**
1. In the linux command line terminal, move to the directory (/testing/Manual_Testing)
2. In the linux terminal, enter the command $python CommandHandlerTest.py
3. When prompted, enter an email address different than the one that will be used to communicate with the system
4. Using an email application, send an email to 'home.suite.home.testing@gmail.com' using an email address 
   different than the one entered into the command line 
**Test Results**
1. The terminal will not show anythin
2. An email message will not be recieved by 'home.suite.home.testing@gmail.com'

# Sensors.py
## Description
Verify *Sensors.py* can properly access sensor data from a web server, convert units and display the results correctly.
## Test Tools and Dependencies 
For this test, we are begining with the following tools installed:
* Atom Text Editor (Or Similar Code Editing Tool)
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
| No. | Steps to Reproduce | Expected Behaviour |
| --- | --- | --- |
| 1 | Open the directory containing both *Sensors.py* and *sensorSim_constant.py* | A folder containing both source files should appear on the screen |
| 2 | Right click in the directory window and select the *Open in Terminal* option | A terminal window will appear with the correct directory showing to the right of the users name |
| 3 | Right click in the directory window for a second time and again select the *Open in Terminal* option | A second terminal window should appear again showing the correct directory name to the right of the users name |
| 4 | In the first terminal window type *python3 sensorSim_constant.py* and press the return key | The terminal window will display the message *Server started ht<span>tp://</span>localhost:8080* |
| 5 | In the second terminal window type *python3 Sensors.py* and press return | The following output will be observed in the terminal: *Temperature in degrees Fahrenheit: 77.0 
Relative Humidity:  
50.0 Dew Point Fahrenheit: 56.93* |

### Edge Case
**Test Status:** *status*
| No. | Steps to Reproduce | Expected Behaviour |
| --- | --- | --- |

**Test Status:** *status*
### Negative Case
| No. | Steps to Reproduce | Expected Behaviour |
| --- | --- | --- |


# posttester.js
1. 
2.  
3.  
