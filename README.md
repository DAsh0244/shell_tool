# Shell Environment for NiDAQmx Compatible products

Allows for control in a command line
shell environment that will allow for shell
command of DAQmx compatible products. 

Will end up supporting:
 - [x] Finite single run reads
 - [x] Multiple file types to save data as ([see here](#ref))
 - [x] Continuous keyboard interrupted reads
 - [ ] Timer based continuous reads
 - [ ] Configurable channel config
 - [ ] Windows
 - [ ] UNIX/LINUX
 
## Requirements

[Python3.x][py] - Tested with `> 3.5.1 Win` , `3.4 Linux`

`pip`

## Installation

[//]: # "Setup virtualenv stuff here if needed" 

Fetch dependencies: 

- Windows: `python -m pip install -r requirements.txt` | `pip install -r requirements.txt` <sup>[1]</sup>

- Linux: `python3 -m pip install -r requirements.txt` | `pip3 install -r requirements.txt` <sup>[2]</sup>

- Mac: `N/A`

[//]: # "setup.py stuff here" 

[//]: # "starting with either bat or sh scripts" 

## Use 

### Windows:
There is a [py_env.bat](src/scripts/py_env.bat) file in the [scripts](src/scripts) directory.
Launch that and follow the dialog to start the tool. 
Recommend making a shortcut to this script for ease of use.

### UNIX/LINUX:
A shell script is in the works. Until then...

Start it by launching `shell.py` with python.  
Must run in the base `shell_tool` directory

eg: `python  src/shell.py` 

### Notes:
There is an optional Command Line Argument `FAKE` 
that allows you to run the shell with the 
[fake_daq](src/utils/fake_daq.py) file for testing of the command line itself

eg: `python  src/shell.py FAKE` 

## Todo 
- Continuous read file chunking for ease of use / in-flight reduncancy
- Preliminary Documentation
- Packaging setup 
- Misc as found

## ref
[1] - assuming you have `python` (and/or `pip`) as Python3 in your `%PATH%`

[2] - assuming you have `python` (and/or `pip`) as Python2 in your `$PATH` already,
as then Python3 should be aliased to `python3`

[3] - currently supported file types:
- `.txt`
- `.csv`
- `.mat`

[//]: # "links"
[py]:https://www.python.org/ "Python main page" 
