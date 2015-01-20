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
- Windows 7 x64
- Windows 8 x64
- Windows 10 x86 
- Rasbian
- Ubuntu

## Development Disclaimer
This code is still very early under development and is not intended for external use and does not represent working
software.

An additional note: I have no prior experience with the python language. This project is a learning project and does
not necessarily represent Python standards or ideal patterns.

## License
This code is available under the GNU General Public License. See LICENSE for more information. 

## Requirements
Pi-MFD requires:
- Python 2.7 or higher
- Pygame
- Pywapi

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
#### Weather (WTHR)
Displays current weather conditions and a 5 day forecast.

Planned improvements:

* Icon support for forecast
* Range Bar support for forecast

### Navigation (NAV)
#### Map (MAP) - Planned
#### Gas (GAS) - Planned
#### Food (FOOD) - Planned
#### Traffic (TRAF) - Planned
#### Weather Conditions (COND) - Planned

### Social (SOC)
#### News (NEWS) - Planned
#### Facebook (FACE) - Planned
#### Twitter (TWTR) - Planned
#### Feedly (RSS) - Planned
#### Browser (WEB) - Planned

### Media (MED)
#### Images (IMG) - Planned
#### Pandora (PAND) - Planned
#### YouTube (TUBE) - Planned
#### Netflix (FLIX) - Planned
#### Amazon Instant Watch (AZIW) - Planned

### System (SYS)

#### System Time (TIME)
Displays the current time in system and GMT time.

#### Performance (PERF)  - Planned
Displays performance metrics for this machine or a machine running WMI.

#### Network (NET) - Planned
#### Options (OPTS)
Allows you to customize application options.

#### Exit (EXIT)
Exits the application

## Future Integrations

### Raspberry Pi

Pi-MFD is currently planned to expand to allow handling of GPIO devices as button handlers and to allow for deployment 
to Android.

Hardware buttons are currently simulated as F1-F5 for top row buttons and F8-F12 for bottom row buttons. F6 and F7 are
reserved for future expansion.

### Resolution Support

The application is currently designed for 800 x 480 as this is the prime deployment target, but support for smaller
displays is planned (down to 320 x 320) as is dynamic resizing.

### User Interface Improvements

The UI framework is very basic at the moment and has notable shortcomings, including mouse, clipboard, and standard
input convention support such as cursors for text boxes and similar touches. This is since mouse and keyboard are
currently treated as second class citizens compared to the hardware buttons that will be in the initial deployment.