![Qwiic I2C Python Package](docs/images/i2c-gh-banner-py.png "qwiic IC Python Package" )

Sparkfun Qwiic I2C - Python Package
==============

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_i2c)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_i2c_py)
![License](https://img.shields.io/github/license/sparkfun/qwiic_i2c_py)
![X](https://img.shields.io/twitter/follow/sparkfun)

Python package to support multi platform I2C bus integrations for the SparkFun [qwiic ecosystem](https://www.sparkfun.com/qwiic)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

## Contents

* [Supported Platforms](#supported-platforms)
* [Dependencies](#dependencies)
* [Documentation](#documentation)
* [Installation](#installation)

Supported Platforms
--------------------
The qwiic I2C Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi) (Single Board Computers)
* [NVidia Jetson Nano](https://www.sparkfun.com/products/15297)
* [Google Coral Development Board](https://www.sparkfun.com/products/15318)

Dependencies 
---------------
The Raspberry Pi/Single Board Computer Linux driver of this package is dependent on 
[smbus](https://pypi.org/project/smbus/)

Documentation
-------------
The SparkFun qwiic I2C module documentation is hosted at [ReadTheDocs](https://qwiic-i2c-py.readthedocs.io/en/latest/index.html)

Installation
---------------

### PyPi Installation
This repository is hosted on PyPi as the [sparkfun-qwiic-i2c](https://pypi.org/project/sparkfun-qwiic-i2c/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-i2c
```
For the current user:

```sh
pip install sparkfun-qwiic-i2c
```
## Local Installation
To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```sh
python setup.py install
```

To build a package for use with pip:
```sh
python setup.py sdist
 ```
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```sh
cd dist
pip install sparkfun_qwiic_i2c-<version>.tar.gz
```

Examples
---------------
This package is used extensively by the python modules for the SparkFun qwiic ecosystem. References to the modules can be found in the [qwiic python package](https://github.com/sparkfun/Qwiic_Py/tree/main/qwiic/drivers)

General package use examples:

```python
# Import the package
import qwiic_i2c

# Get the default I2C bus
my_bus = qwiic_i2c.get_i2c_driver()

# Linux (Raspberry Pi) - Specify I2C bus index
my_bus = qwiic_i2c.get_i2c_driver(iBus = 1)

# MicroPython and CircuitPython - Specify SDA and SCL pins, and frequency
my_bus = qwiic_i2c.get_i2c_driver(sda=0, scl=1, freq=100000)

# Perform scan of I2C bus
scan_list = my_bus.scan()
print("Bus scan:", scan_list)

# Check if a device with the specified address is connected
ping_result = my_bus.ping(device_address)
print("Device is connected:", ping_result)

# Read one byte from the specified address
read_data = my_bus.read_byte(device_address, register_address)
print("Read byte:", read_data)

# Read one word (2 bytes) from the specified address
read_data = my_bus.read_word(device_address, register_address)
print("Read word:", read_data)

# Read several bytes from the specified address
read_data = my_bus.read_block(device_address, register_address, num_bytes_to_read)
print("Read block:", read_data)

# Write one byte to the specified address
my_bus.write_byte(device_address, register_address, write_data)

# Write one word (2 bytes) to the specified address
my_bus.write_word(device_address, register_address, write_data)

# Write several bytes to the specified address
my_bus.write_block(device_address, register_address, write_data)
```

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
