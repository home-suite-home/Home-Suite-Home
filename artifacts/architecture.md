

# Program Organization
Home-Suite-Home is an open-source sensor suite. It is designed to be lightweight, modular home
analytics suite that provides home-owners and property managers a platform to monitor the health of their properties through the useof smart sensors. On a high level of operation, the sensors are responsible for sending data to a localised database hosted by a server/agregator. The sever portion stores data for time-series representaton, and he aggregator portion observes values in real time to verify that sensor readings are within user defined parameters. The user will recieve notfications via email in the event of any data anomolies, or when requested for data snapshots or historical data.

# Code Design

# Data Design

# Business Rules
- The system should record new sensor data every 30 seconds.
- The user should be able to add new sensors after initial setup through the GUI.
- The system should be able to store at least a year's worth of sensor data. This should be
calculated with a 'standard' sensor collection.

# User Interface Design
![UI to get the user's email](assets/screenshot_email_ui.png)
The purpose of this screen is to get the user's email so that the raspberry
pi knows where to send updates and statistics about the user's system.

The user uses the mouse to click on the text box, and then they type their
email. Once the user presses submit, a confirmation email is sent to the user so that they know that sending an email works.

| Window Number | UID |
|---------------|-----|
| 1             | 011 |

# Resource Management
Computational load is divided among several ESP8266 modules with 2.5GHz? processors, and a
Raspberri Pi 3 with 2Gb? of RAM. The Pi is responsile for running the main script for the aggregator,hosting the GUI and related config files, as well as hosting the database forthe sensors. Further research is needed to determine the exact workload and resurce requirements 

# Security
This solution is designed to focus on ease of access and utility to the open-source community.
That said software security is not a primary concern for our implementation. The architecture of the system however, lends itself to being rather secure in practice. All traffic occurs over the local network, and so the data saved within the database is not seen except by those on said network.

# Performance

# Scalability
The user will be able to add extra sensors up to a point, so as t provide greater breadth of analytics. A single instance of the system can serve only proprty due to the localised nature of operation.

# Interoperability
The sensors are responsible for sharing data with the database as well at the aggregator.

# Internationalization/Localization

# Input/Output

# Error Processing

# Fault Tolerance

# Architectural Feasibility

# Overengineering

# Build-vs-Buy Decisions

# Reuse

# Change Strategy


