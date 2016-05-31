# PyOptoSigma
Python module for operating stepping moter stages manufactured by OptoSigma and Sigma Koki.

シグマ光機（OptoSigma）のステージコントローラを Python で制御するモジュール．

# Dependencies installation

This module depends on ```python3``` and ```pyserial```.
Please note that the supported Python version is 3.4 or greater, and Python 2.x, 3.1, 3.2, and 3.3 are not supported.

In Ubuntu 14.04, you should install python3 packages first.
```
 sudo apt-get install python3-pip
```
And then install ```pyserial``` via pip.
```
 sudo pip3 install pyserial
```

To access to serial ports without sudo privileges, the user must belong to  ```dialout``` group.
```
 sudo gpasswd -a [user_name] dialout
```
where, [user_name] is the user name, which can be confirmed by ```id``` command.

# Install

There are two ways to install this module.

1. Use pip
 ```
  sudo pip3 install pyOptoSigma
 ```
 
2. From source
 ```
  git clone https://github.com/ken1row/PyOptoSigma.git
  cd PyOptoSigma
  sudo python3 install.py install
 ```

# Get started

The following code (python3) will work for example, to rotate 45 degree.
```
 from pyOptoSigma import *
 stages = Session(Controllers.SHOT_702)     # specify your stage controller.
 stages.append_stage(Stages.SGSP_120YAW)    # add your stage accordingly.
 stages.connect()                           # connect to a serial port.
 stages.move(amount=45000)                  # rotate 45 degree.
```

# Build API Documents
Documents can be generated using ```sphinx```. Firstly, install the latest sphinx via pip.
```
sudo pip install sphinx --upgrade
```

Then, compile documents using sphinx.
```
make html
```

Documents will be generated in ```build/html``` directory.


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
