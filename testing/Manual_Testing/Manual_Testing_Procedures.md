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
### [U014] As a property owner I want to receive a response from the system when a command is given over email so that the system will do what I want remotely.
### Functional Case (help message)
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

### [U003] As a property owner, I would like to view a graphic representation of sensor data over time so that I can see trends in my property.
### Functional Case (get sensor data)
**Test Status** *PASS*</br>
#### Test Procedures
| No. | Steps to Reproduce | Expected Behavior |
| --- | --- | --- |
| 0 | Have a mongodb instance running locally on your machine | ![mongo](/artifacts/assets/instance_mongodb.png) |
| 1 | Import the test database into mongodb instance | ![import](/artifacts/assets/import_mongodb.png)
| 2 | In the linux command line terminal, from the repo's main directory, move to the manual testing directory| ![cd](/artifacts/assets/move_to_testing.PNG) |
| 3 | In the linux terminal, enter the command $python CommandHandlerTest.py | ![prompt](/artifacts/assets/CommandHandlerCommand.PNG) |
| 4 | Using an email application, send an email to 'home.suite.home.testing@gmail.com' from 'home.suite.home.test.user@gmail.com'| ![test_request](/artifacts/assets/get_data_email.png) |

#### Test Results
| No. | Expected Results | Actual Results |
| --- | --- | --- |
| 1 | The terminal will reflect the operations being handled by the running program | ![terminal_response](/artifacts/assets/terminal_email.png) |
| 2 | An email message will be recieved by 'home.suite.home.testing@gmail.com' conatining an image of the data graph| ![email_response](/artifacts/assets/email_graph.png) |

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
## [U002] As a property-owner, I'd like the temperature of my property to be monitored.
## Description
Verify *Sensors.py* can properly access sensor data from a web server, convert units and display the results correctly.
## Test Tools and Dependencies
For this test, we are beginning with the following tools installed:
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

# Database_test.py
## [DEV015] As a developer, I want to be able to access the database in Python, so that I can use database functions in other python files.  
## Description
This test script works to interact with the MongoDB database that will house the records for all of our sensors. The purpose of this script is to prove that we have connection to the database and can make edits to it without going through the database's GUI.

## Testing Requirements and Dependencies
To set up a test environment in which to run the code, the following tools are required:

* Bash shell(or a similar Unix terminal emulator)
* [MongoDB Community Server](https://www.mongodb.com/try/download/community)
* [Database.py](/source/Server_Component/Database.py)
* [Database_test.py](/testing/Manual_Testing/Database_test.py)
* [timeKeeper.py](/source/timeKeeper.py)

Before running any of the programs listed here, it is recomended to follow the procedures for [setting up the server process for MongoDB](https://docs.mongodb.com/manual/administration/install-community/) on your operating system. If you want access to a GUI for the database, it is recommended that you choose to install on either macOS or Windows. Ensure that *Database_test.py*, *Databse.py*, and *timeKeeper.py* are in the same directory on your machine before running.

## Test Procedures

| No. | Steps to Reproduce | Expected Behavior |
| --- | --- | --- |
|  1  | Open the file *Database_test.py* on a text editor of your choice, and uncomment the lines db.clearConfigData() and db.clear() if they are not already. | The line will light up to indicate that it will be compiled when ran. |
|  2  | Open the terminal and procede to the directory containing the required files. | The directory should contain both files required for testing when inputting the commands *ls* or *dir* on the command line. |
|  3  | Run the *Database_test.py* script | Upon opening the MongoDB GUI (if running on macOS or Windows) you should see an empty databse called *sensorsdb* ![empty](/artifacts/assets/empty_sensorsdb.PNG) |
|  4  | Return to the *Database_test.py* file and now comment out the lines db.clearConfigData() and db.clear(). | The line should now appear commented out and it will not compile when ran in the command line. |
|  5  | Run the testing script again. | The command line shall have a view of the config data before and after deleting elements from it. ![configDel](/artifacts/assets/config_delTest.PNG) |
|  6  | Scroll down on the terminal. | The command line shall have have a view of all the records as a list and should also be printing the averages for each sensor. ![cmd](/artifacts/assets/cmd_dbTest.PNG) |
|  7  | Scroll down on the terminal. | The terminal shall show 20 timestamps strings in epoch time. It will also show the 5 most recent objects passed to the database and their corresponding epoch time. ![recent](/artifacts/assets/getRecent_test.PNG)|
|  8  | Check the Database once again. Two collectons should be added. Click the one named *config*.  | The database should be populated with the sensor configuration data sent in the testing file! ![config](/artifacts/assets/config_db.PNG)|
|  9  | Click the second collection named *sensors*.| The database should now be populated with the sensor data sent in the testing file. ![populated](/artifacts/assets/populated_sensorsdb.PNG)|


# Database Maximum Certified Usage
## [U021] As a property owner, I want to have a history for up to 100 sensors over a time period of one year so that, I may look back on trends in my historical sensor data.
## Description
This procedure will test the stability of the database and certify the ability to contain data to satisfy the following maximum specifications guidelines:

* 100 individual sensors
* Polling rate of all sensors is once per minute
* 1 year of data (45,000) entries must be searchable in less than 30 seconds

Note: The systems preformed nominally under these conditions and likely has the capability to scale beyond these guidelines.

## Test Tools and Dependencies
For this test, we are beginning with the following tools installed:
* Linux Text Editor (Or Similar Code Editing Tool)
* Linux Command Line
* Raspberry Pi 4 8gb running Ubuntu 20.10

We will also need the following test scripts:
* [Database_stressAdd_1000.py](/testing/Manual_Testing/Database_Stress_Test/Database_stressAdd_1000.py)
* [Database_stressSearch.py](/testing/Manual_Testing/Database_Stress_Test/Database_stressSearch.py)
* [Database.py](/testing/Manual_Testing/Database_Stress_Test/Database.py)
* [Sensors.py](/testing/Manual_Testing/Database_Stress_Test/Sensors.py)

## Test Case
**Test Status:** *PASS*

**Note:** The steps in this procedure should be carried out on a Raspberry Pi as specified in Tools for this section.
| No. | Steps to Reproduce | Expected Behavior |
| --- | --- | --- |
| 1 | Download all source scripts and place them in the same folder together | All source scripts needed for testing will be in the same directory |
| 2 | Open the directory containing all source scripts for this test | A directory listing all source files shall appear on the user's screen |
| 3 | Right click in the folder window with the testing source files and select *open in terminal* from the context menu | A terminal window shall open and display the correct file path next to the user's username |
| 4 | Type *python3 Database_stressAdd_1000.py* and press return | The script shall begin populating the database. This may take approx. 170 minutes |
| 5 | Once the script from step 4 has finished running type *time python3 Database_stressSearch.py* and press return | The average value for one sensor of the database shall be calculated representing a technical worst case for access time |
| 6 | Observe the *real* time printed in the terminal window and ensure that time is less than 60 seconds | The *real* time the Database took to return the average value will be less than 60 seconds ![searchTime](/artifacts/assets/database_sressSearch.png) |


# Sensor Configurations in the Database
## [U019] As a property owner, I would like to save my sensor preferences so that, I only have to enter the information for each sensor once.

## Description
This procedure will demonstrate manually loading and retrieving the user settings configurations for each sensor.

## Test Tools and Dependencies
For this test, we are beginning with the following tools installed:
* Linux Text Editor (Or Similar Code Editing Tool)
* Linux Command Line
* Raspberry Pi 4 8gb running Ubuntu 20.10

We will also need the following test scripts:
* [databse_config_populate.py](/testing/Manual_Testing/Sample_Database/databse_config_populate.py)
* [database_read_configs.py](/testing/Manual_Testing/Sample_Database/database_read_configs.py)
* [Database.py](/source/Server_Component/Database.py)

## Test Case
**Test Status:** *PASS*
| No. | Steps to Reproduce | Expected Behavior |
| --- | --- | --- |
| 1 | Open the directory containing all three source scripts for testing | A directory containing the scripts we are using for this test will appear |
| 2 | Right click in the directory and select *open in terminal* from the context menu | A terminal window with the correct file path next to the user's username will appear |
| 3 | Type *python3 databse_config_populate.py* and press return | The script should compile and run without any errors |
| 4 | Once the script in step 3 has finished running, type *python3 database_read_configs.py* | all of the configuration data added in the previous step will be printed to the terminal |


# sensor_driver.py
## [U022] As a homeowner, I want multiple temperature and humidity sensors to save their readings so that, I can retain the historical environment data around my property.

## Description
This procedure will demonstrate the capability to save sensor data to the database at a regular interval.

## Test Tools and Dependencies
For this test, we are beginning with the following tools installed:
* Linux Text Editor (Or Similar Code Editing Tool)
* Linux Command Line
* A database loaded with sensor configurations
* A set of sensors

We will also need the source code:
* [sensor_driver.py](/source/sensor_driver.py)

## Test Case
**Test Status:** *PASS*
| No. | Steps to Reproduce | Expected Behavior |
| --- | --- | --- |
| 1 | Open the directory containing the source file | A directory containing *sensor_driver.py* will appear |
| 2 | Right click in the directory containing the source file for testing and select *open in terminal* from the context menu | A terminal window with the correct file path displayed next to the user's username will appear |
| 3 | Type *python3 sensor_driver.py* and press return | *sensor_driver.py* will compile and run |
| 4 | Observe the printouts to the terminal windows | each time a sensor is accessed and recorded, a printout containing the senor name and value to record is displayed in the terminal window |
| 5 | The script will loop every 60 seconds gathering data until we interrupt it - press *ctrl + c* to stop the script | The terminal window will return control to the user showing the test has ended |
