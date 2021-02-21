This file contains instructions for executing manual testing 

# CommandHandlerTest.py 
1. 
2. 
3. 

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
| 5 | In the second terminal window type *python3 Sensors.py* and press return | The following output will be observed in the terminal: ![Sensor.py Nominal Output](/artifacts/assets/sensor_py_output.PNG)|

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
