# Pi-MFD

## Overview
This project is an attempt to build a Python-based dashboard application that works with a 7 inch Raspberry Pi display. 
This came out of a desire to tinker with Raspberry Pi, learn Python and become more exposed to Unix and Physical computing.

## Current Status
The application is essentially a loose framework of display components that does not allow for user-interactivity.

## Deployment Target
The intended deployment target of this software during development is a ThermalTake Core V1 mini-atx case hosting a 
Raspberry Pi B+ running Raspbian and outputting on a 7 inch external display. The display is augmented with 5 hardware
buttons mounted above and below the case.

## Development Disclaimer
This code is still very early under development and is not intended for external use and does not represent working software.

An additional note: I have no prior experience with the python language.

## License
This code is available under the GNU General Public License. See LICENSE for more information. 

## Requirements
Pi-MFD requires:
    * Python 2.7 or higher
    * A version of pygame compatible with the installed version of Python.

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

### Number Pad
The number pad allows for interaction with the current page, including navigating up, down, left, right, and selecting items.
The keypad will not allow users to select items on the top or bottom row.
    
## Features
Pi-MFD is planned to integrate several disparate application modules and display dashboard information for each module.

Planned applications and their pages are listed as follows:

### Scheduling (SCH)
#### Tasks (TASK) - Planned
#### Mail (MAIL) - Planned
#### Calendar (CAL) - Planned
#### Weather (WTHR) - Planned

### Navigation (NAV)
#### Map (MAP) - Planned
#### Gas (GAS) - Planned
#### Food (FOOD) - Planned
#### Traffic (TRFC) - Planned
#### Weather Conditions (COND) - Planned

### Social (SOC)
#### News (NEWS) - Planned
#### Facebook (FACE) - Planned
#### Twitter (TWTR) - Planned
#### Feedly (RSS) - Planned
#### Browser (WEB) - Planned

### Media (MED)
#### Images (IMG) - Planned
#### YouTube (TUBE) - Planned
#### Netflix (FLIX) - Planned
#### Hulu (HULU) - Planned
#### Amazon Instant Watch (AZIW) - Planned

### System (SYS)

#### Clock (CLK) - Done
Displays the current time in system and GMT time.

#### Performance (PERF)  - Planned
#### Network (NET) - Planned
#### Options (OPTS) - Planned
#### Exit (EXIT) - Planned
Exits the application