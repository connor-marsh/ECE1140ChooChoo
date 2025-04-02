# ECE1140ChooChoo
### Installation Instructions
Clone this repository locally
Install anaconda, open an anaconda powershell prompt through the anaconda navigator.
Navigate in that powershell to this github repositories cloned location, then run this command:
`conda env create -f environment.yml`

### Adding modules
To add a new module, run this command:
`conda install -c conda-forge [module_name]=[module_version]`
Then to update the environment.yml file, run this command:
`conda env export > environment.yml`
***Then remove the prefix line, which is specific to your computer. After that you are good to commit the new environment file.***
