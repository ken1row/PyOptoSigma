# PyOptoSigma
Python module for operating stepping moter stages manufactured by OptoSigma and Sigma Koki

シグマ光機（OptoSigma）のステージコントローラを Python で制御するモジュール．

# Dependencies

This module depends on ```python3``` and ```pyserial```.
In Ubuntu 14.04, you should install python3 packages first.
```
 sudo apt-get install python3-pip
```
And then install ```pyserial``` via pip.
```
 sudo pip3 install pyserial
```

# Get started

Copy all python scripts to your current directory.
The following code (python3) will work for example, to rotate 45 degree.
```
 import pyOptoSigma
 stages = pyOptoSigma.Session(Controllers.SHOT_702) # specify your stage controller.
 stages.append_stage(Stages.SGSP_120YAW) # add your stage accordingly.
 stages.connect()
 stages.move(amount=45000) # rotate 45 degree
```

# See also
* Documentation is under construction (See Issues).
* A test code written at the end of ```pyOptoSigma.py``` will help more operations.

# Confirmed Environments
Listed below are confirmed to work propery. But this module is not limited to the listed equipments.

## Controllers
* SHOT-702
* SHOT-304GS

## Stages
### Linear translation stages
* SGSP26-150
* SGSP33-200
* SGSP46-500
* SGSP46-800

### Rotation stages
* SGSP-120YAW

## OS
* Ubuntu 14.04.2
