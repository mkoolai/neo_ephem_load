# NEO ephemeris load #

_neodys_ephem.py_ is a python script which downloads NEODyS ephemeris files from [NEODyS-2]( https://newton.spacedys.com) website. The script automatically fills observational query on webpage https://newton.spacedys.com/neodys/index.php?pc=3.2, saves result into temporary file neodys_lst.html and for each item in the list of objects downloads ephemeris as ASCII table with file extention "neo". Input parameters used for query are in configuration file 'neodys.ini'. Command line input argument is path to directory where to save results.

Example of execution:
    ./neodys_ephem.py $save_path

_neo_auto.sh_ is a shell script which executes neodys_ephem.py and saves the results into directory with current date name.
