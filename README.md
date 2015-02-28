# Pi-MFD

## Overview
This project is an attempt to build a Python-based dashboard application that works with a 7 inch Raspberry Pi display. 
This came out of a desire to tinker with Raspberry Pi, learn Python and become more exposed to Unix and Physical computing.

## Current Status
The application is essentially a loose collection of partially implemented modules with a simple navigation capability 
using mouse buttons or F1-F5 and F8-F12 keys.

## Deployment Target
The intended deployment target of this software during development is a custom case hosting a Raspberry Pi B+ running
Raspbian and outputting on a 7 inch Sainsmart external display with a 800 x 480 resolution. The display is augmented
with 5 hardware buttons mounted above and below the case.

### Compatible Platforms
Pi MFD has been tested in its current state on the following platforms: 

* Windows 7 x64
* Windows 8 x64
* Windows 10 x86 
* Rasbian
* Ubuntu

## Development Disclaimer
This code is still very early under development and is not intended for external use and does not represent working
software.

An additional note: I have no prior experience with the python language. This project is a learning project and does
not necessarily represent Python standards or ideal patterns.

## License
This code is available under the GNU General Public License. See LICENSE for more information. 

## Requirements
Pi-MFD requires:

* Python 2.7
* Pygame

### Optional - Needed for Full Functionality
* xmltodict
* WMI
* Pywin32 - http://sourceforge.net/projects/pywin32/files/
* psutil - https://github.com/giampaolo/psutil/

## User Interface

### Principles
Pi-MFD intentionally goes for a toned down military / console style of user interface inspired somewhat by avionics
displays found on modern aircraft. The application should feel as a whole like a ruggedized / spartan dashboard application.

Ease of learning should intentionally not be a prime concern.

### Top Row
The top row relates to the current application or application silo and allows users to change contexts.

### Bottom Row
The bottom row relates to pages inside the current application stack.
Pressing on a page when it is already selected will allow the user to 

### Left Side
The left side buttons are currently unsupported

### Right Side
The right side buttons are currently unsupported

### Number Pad
The number pad allows for interaction with the current page, including navigating up, down, left, right, and selecting items.
The keypad will not allow users to select items on the top or bottom row.
    
## Features
Pi-MFD is planned to integrate several disparate application modules and display dashboard information for each module.

Applications and their pages are listed as follows:

### Core (CORE)
Contains core application functionality intertwining the entire system.

#### Home (HOME)
Contains information dashboard widgets from all applications.

#### Info (INFO)
Displays system information.

#### Options (OPTS)
Allows you to customize application options.

#### Exit (EXIT)
Exits the application

### System (SYS)

#### Performance (PERF)
Displays performance metrics for the application.

#### Drives (DRVS)
Displays disk drives detected and allows you to drill down into a drive.

#### Service (SRVC)
Lists active services on the WMI computer being monitored. This requires a workable WMI. 

#### Processes (PROC)
Lists active process on the machine and allows the user to drill down into more details.

#### Connections (CONN)
Lists active network connections on the machine and allows the user to jump to the process associated with the connection.

### Navigation (NAV)
Displays a representation of the world map using OpenStreetMaps data based on the Lat / Long configured in the settings
file. Page / Pan using the arrow keys. Filter the map by toggling the map button. Move to pan / cursor mode by toggling
the Page / Pan / Cur button. Move the cursor in cursor mode via mouse click or arrow keys. Drill into details for the
selected node by clicking info when a node is selected.

Weather nodes will display that area's weather data.

Nodes with images or webcam feeds will display that image (and allow fullscreen view). Nodes with an image and an
interval tag will auto-refresh (useful for traffic and weather cameras).

Traffic accidents and construction from Bing Maps will be displayed.

GOTO allows the user to manage locations and jump to specific locations as well as add, delete, and edit locations.

### Scheduling (SCH)
The scheduling application contains components related to scheduling, communication, and notification.

#### Tasks (TASK) - Planned
#### Mail (MAIL) - Planned
#### Calendar (CAL) - Planned
#### Weather (WTHR)
Displays current weather conditions and a 5 day forecast.