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

### Train Model UI

### Train Controller SW UI

### Train Controller HW UI

## Common User Errors
1. hello
2. hello 2
3. hello 3
