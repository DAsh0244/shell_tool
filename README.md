# Shell Environment for NiDAQmx Compatible products

Allows for control in a command line
shell environment that will allow for shell
command of DAQmx compatible products. 

Supports:
 - [x] Finite single run reads
 - [ ] Continuous keyboard interrupted reads
 - [ ] Timer based continuous reads
 - [ ] configurable channel config
 - [ ] multiple file types to save data as
 
##Requirements
[Python3.x][py] - Tested with `> 3.5.1 Win` , `3.4 Linux`

pip

## Installation

[//]: # "Setup virtualenv stuff here if needed" 

Fetch dependencies: 

- Windows: `python -m pip install -r requirements.txt` | `pip install -r requirements.txt` <sup>[1]</sup>

- Linux: `python3 -m pip install -r requirements.txt` | `pip3 install -r requirements.txt` <sup>[2]</sup>

- Mac: `N/A`

[//]: # "setup.py stuff here" 

[//]: # "starting with either bat or sh scripts" 

## Use 
Start it by launching `shell.py` with python. 
eg: `python shell.py` 

##Todo - first Build
- [ ] Front End Functions
- [ ] Backend Functions
- [ ] Preliminary Documentation
- [ ] Packaging setup


- [ ] Misc as found

##ref
[1] - assuming you have `python` (and/or `pip`) as Python3 in your `%PATH%`

[2] - assuming you have `python` (and/or `pip`) as Python2 in your `$PATH` already,
as then Python3 should be aliased to `python3`

[//]: # "links"
[py]:https://www.python.org/ "Python main page" 
