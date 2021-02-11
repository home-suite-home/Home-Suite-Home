

# Program Organization

# Code Design

# Data Design

# Business Rules
---
- The system should record new sensor data every 30 seconds.
- The user should be able to add new sensors after initial setup through the GUI.
- The system should be able to store at least a year's worth of sensor data. This should be
calculated with a 'standard' sensor collection.

# User Interface Design

# Resource Management
---
Computational load is divided among several ESP8266 modules with 2.5GHz? processors, and a
Raspberri Pi 3 with 2Gb? of RAM. The Pi is responsile for running the main script for the aggregator,hosting the GUI and related config files, as well as hosting the database forthe sensors. Further research is needed to determine the exact workload and resurce requirements 
# Security
---
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


