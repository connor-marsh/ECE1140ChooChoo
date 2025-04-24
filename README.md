# ECE1140ChooChoo - Team Choo Choo Train System

## MEMBERS:
| Name | Module |
| ----------- | ----------- | 
| Aaron Kuchta | CTC |
| Connor Murray | SW Track Controller |
| PJ Granieri |  Track Model |
| Iyan Nekib |  Train Model |
| Aragya Goyal | SW Train Controller |
| Connor Marsh | HW Train Controller |

## Project Description
Code for ECE1140: Systems and Project Engineering, informally known as "Trains". Project consists of creating a simulation of the entire Pittsburgh Regional Transit Railway, with a deep focus on proper Systems Engineering methodology.

## Documentation
For the project, our team created IEEE documents following the IEEE 828, 829, 830 and 1016 standards. Our team has also created a coding standards document and this help guide.

## Deployment
### Installation Instructions
Clone this repository locally
Install anaconda, open an anaconda powershell prompt through the anaconda navigator.
Navigate in that powershell to this github repositories cloned location, then run this command:
`conda env create -f environment.yml`

### Adding packages
To add a new package, run this command:
`conda install -c conda-forge [module_name]=[module_version]`
Then to update the environment.yml file, run this command:
`conda env export > environment.yml`
***Then remove the prefix line, which is specific to your computer. After that you are good to commit the new environment file.***

### Raspberry Pi Setup

## Usage
### Starting the Simulation

### Dispatching a Train

## UI Descriptions
### CTC UI
The Centralized Traffic Control (CTC) user interface is organized into three main sections and four functional subsections. Upon launch, the interface defaults to displaying the Green Line on the main screen.
#### Top Bar Features:
- Active Train Counter – Displays the number of currently active trains.
- Line Selector Slider – Switches between the Green and Red lines.
- Maintenance Mode Toggle – Enables or disables maintenance controls.
- 12-Hour Clock – Provides real-time timekeeping.
#### Main Interface Layout:
#### Left Section (Track View):
- Displays a visual representation of the currently active track. Users can select individual blocks from this view or from the adjacent table to view specific details, including Block ID, speed limit, and length. The line's total throughput is also shown here. In Maintenance Mode, a large dial becomes available to manually change the state of track switches.
#### Right Section (Train Table):
- Displays real-time information about all active trains. Navigation buttons allow users to access the four functional subsections
#### Subsections:
#### Dispatch Train
Allows users to dispatch trains from the yard.
- Dispatch Type: Choose between dispatching a new train or rerouting an existing one.
- Destination Type: Select a route, station, or specific block.
- Once selections are made, the dispatch button becomes active to initiate the process.

#### Select Train
Enables manual control of any active train.
- Users input desired authority and speed, which are validated to prevent unsafe entries.
- Once submitted, the train is marked as being in manual mode via a radio button indicator.

#### Maintenance
Provides block maintenance functionality.
- After enabling Maintenance Mode via the top bar, users can select blocks and toggle their maintenance status using "Start Maintenance" and "End Maintenance" buttons.

#### Upload Schedule
Opens a file explorer dialog allowing the user to upload a schedule file.
- The selected file is then parsed and integrated into the train scheduling system.
- This feature supports automated train dispatching and timeline-based coordination based on pre-configured schedules.
### Wayside Controller UI

### Track Model UI
The Track Model user interface allows for dynamic visualization and interaction with the selected transit line. It supports both the Green and Red Lines and provides real-time feedback for block data, infrastructure status, temperature, and failure simulation.

#### Top Bar Features:
- Import Track Layout – Opens a file dialog to upload an updated `.xlsx` or `.xls` layout file. The file must match the selected line and contain "Green" or "Red" in cell A2.
- Line Selector Dropdown – Switches between the Green and Red lines.
- Block Selector Dropdown – Allows selection of individual blocks by ID.
- 12-Hour Clock – Displays the current system time.
- Simulation Speed Input – Adjusts how quickly the simulation runs.
- Temperature Input – Accepts user input for track temperature.
- Track Heaters Display – Automatically updates based on the temperature to show whether heaters are enabled or disabled.

#### Main Interface Layout:
#### Center Section (Track Layout Map):
- Displays a zoomable, interactive map of the currently selected line.
- Users can click on individual blocks to view their data or select them via the dropdown.
- Real-time infrastructure icons appear on the map, including trains, stations, switches, signal lights, crossings, and failure indicators.
- Block occupancy and failure states are visually reflected on the map.

#### Bottom Left Section (Block Data):
- Shows detailed attributes for the currently selected block, including:
  - Block ID
  - Block Length (yd)
  - Speed Limit (mph)
  - Wayside Speed (if available)
  - Wayside Authority (if available)
  - Grade (%)
  - Elevation (yd)
  - Underground Status
  - Direction of Travel
  - Beacon Status
  - Railway Crossing Status

#### Bottom Center Section (Key):
- Displays a legend for interpreting icons shown on the track layout map.
- The following icons are included:
  - Train
  - Station
  - Switch
  - Signal Light
  - Railway Crossing
  - Maintenance Indicator
  - Track Circuit Failure
  - Broken Rail Failure
  - Power Failure

#### Bottom Right Section (Failure Modes and Selected Object Information):
- Failure Modes:
  - Toggle individual block failures using the "Edit" buttons:
    - Track Circuit Failure
    - Broken Rail Failure
    - Power Failure
  - Use the "Reset Errors" button to clear all failures on the map.

- Selected Object Information:
  - When an infrastructure icon is clicked, its data is displayed.
    - Train – Displays location, speed, authority, direction, and passenger count.
    - Station – Displays name, ticket sales, boarding, and departing counts.
    - Switch – Displays connected blocks and current route.
    - Signal Light – Shows current signal state.
    - Railway Crossing – Indicates whether the crossing is active or inactive.

### Train Model UI

### Train Controller SW UI

This user interface provides real-time monitoring and control capabilities for a train controller system. It is organized into distinct sections for intuitive interaction and quick access to critical information.

#### Train Selection
- **Train ID:** Dropdown menu to select which train to monitor and control.

#### Auxiliary Controls
- **Headlights & Interior Lights:** Toggle controls for turning on/off lighting systems.
- **Doors:** Buttons to control the opening and closing of left and right-side train doors.
- **Cabin Temperature:** Displays and allows adjustment of the cabin temperature in Fahrenheit.

#### Train Information
- **Actual Speed:** Displays the current speed of the train (in mph).
- **Speed Limit:** Displays the current track speed limit (in mph).
- **Commanded Power:** Shows the power command sent to the train (in kW).
- **Target/Input Speed:** Allows manual input of a desired speed and applying it in manual mode (in mph).
- **Service Brake:** Toggle control for applying or releasing the service brake. There are also lights to display whether the service brake is applied or not.
- **Authority:** Displays the remaining travel authority (distance permitted in yards).

#### Failure Box
- Displays the current status of:
  - **Signal Failure**
  - **Brake Failure**
  - **Engine Failure**
- Includes a large **Emergency Stop** button to trigger an emergency stop or response.

#### Announcements and Miscellaneous
- **Next Station:** Display for the upcoming station.
- **Global Clock:** Displays the current system time in 12-hour format.

#### Control Constants
- **Kp & Ki Values:** Fields to view or adjust the proportional and integral gain constants used for control logic. To be accessed by the Train Engineer. Once these are applied - they cannot be changed.

#### Control Mode
- Allows switching between **Automatic** and **Manual** control modes. This will enable/disable some controls depending on which mode you are in.

#### Notes regarding Train Controller
- Once service brake are applied in manual mode, the driver must untoggle the service brakes in order for the train to move since you are in manual mode.


### Train Controller HW UI

## Common User Errors
1. hello
2. hello 2
3. hello 3
