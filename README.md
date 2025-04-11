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

### Wayside Controller UI

### Track Model UI

### Train Model UI

### Train Controller SW UI

### Train Controller HW UI

## 