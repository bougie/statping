statping
========
stat ping is a ping monitoring tool very simple and very light.

## Installation
```
# aptitude install python-rrdtool fping python-flup
# mkdir data
# mkdir public/graphs
```

## Configuration
### Hosts list
Hosts that you want to chek have to be inserted in the **confs/hosts** file. One host by line and that's all.

### Other configuration items
For ocnfigurate ping command, data direcrories, etc, it's in **confs/config.py** file.

## Running
To collecte values, run periodicly :
```
# python bin/collect.py
```

To view collected values, simply run the embded webserver :
```
# python public/statping.py
```
