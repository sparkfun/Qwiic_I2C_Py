#-----------------------------------------------------------------------------
# linux_i2c.py
#
# Encapsulate the Linux Plaform bus interface
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================

from __future__ import print_function

from .i2c_driver import I2CDriver

import sys


_PLATFORM_NAME = "Linux"

#-----------------------------------------------------------------------------
# Internal function to connect to the systems I2C bus.
#
# Attempts to fail elegantly - often an issue with permissions with the I2C 
# bus. Users of this system should be added to the system i2c group
#
def _connectToI2CBus():

	try:
		import smbus
	except Exception as ee:
		print("Error: Unable to load smbus module. Unable to continue", file=sys.stderr)
		return None

	iBus = 1
	daBus = None

	error=False

	# Connect - catch errors 

	try:
		daBus =  smbus.SMBus(iBus)
	except Exception as ee:
		if(type(ee) is IOError and ee.errno == 13):
			print("Error:\tUnable to connect to I2C bus %d: Permission denied.\n\tVerify you have permissoin to access the I2C bus" % (iBus), file=sys.stderr)
		else:
			print("Error:\tFailed to connect to I2C bus %d. Error: %s" % (iBus, str(ee)), file=sys.stderr)

		# We had an error.... 
		error=True

	# below is probably not needed, but ...
	if(not error and daBus == None):
		print("Error: Failed to connect to I2C bus %d" % (iBus), file=sys.stderr)

	return daBus


# notes on determining Linux platform
#
# - sys.platform == 'linux' or 'linux2', os.uname ->> res.sysname or res[0]=='Linux'
#	## Means it's a linux system - and we support it
#
# To find out a particular system:
#
# 	- Need to start looking at particular hardware classes in /proc/cpuinfo
# 
class LinuxI2C(I2CDriver):

	# Constructor
	name = _PLATFORM_NAME

	_i2cbus = None

	def __init__(self):

		# Call the super class. The super calss will use default values if not 
		# proviced
		I2CDriver.__init__(self)



	# Okay, are we running on a Linux system?
	@classmethod
	def isPlatform(cls):

		return sys.platform in ('linux', 'linux2')


#-------------------------------------------------------------------------		
	# General get attribute method
	#
	# Used to intercept getting the I2C bus object - so we can perform a lazy
	# connect ....
	#
	def __getattr__(self, name):

		if(name == "i2cbus"):
			if( self._i2cbus == None):
				self._i2cbus = _connectToI2CBus()
			return self._i2cbus

		else:
			# Note - we call __getattribute__ to the super class (object).
			return super(I2CDriver, self).__getattribute__(name)

	#-------------------------------------------------------------------------
	# General set attribute method
	#
	# Basically implemented to make the i2cbus attribute readonly to users 
	# of this class. 
	#
	def __setattr__(self, name, value):

		if(name != "i2cbus"):
			super(I2CDriver, self).__setattr__(name, value)

#-------------------------------------------------------------------------	
	# read Data Command

	def readWord(self, address, commandCode):

		return self.i2cbus.read_word_data(address, commandCode)		


	def readByte(self, address, commandCode):
		return self.i2cbus.read_byte_data(address, commandCode)				

	def readBlock(self, address, commandCode, nBytes):
		return self.i2cbus.read_i2c_block_data(address, commandCode, nBytes)

		
	#--------------------------------------------------------------------------	
	# write Data Commands 
	#
	# Send a command to the I2C bus for this device. 
	#
	# value = 16 bits of valid data..
	#

	def writeCommand(self, address, commandCode):

		return self.i2cbus.write_byte(address, commandCode)

	def writeWord(self, address, commandCode, value):

		return self.i2cbus.write_word_data(address, commandCode, value)


	def writeByte(self, address, commandCode, value):

		return self.i2cbus.write_byte_data(address, commandCode, value)

	def writeBlock(self, address, commandCode, value):

		# if value is a bytearray - convert to list of ints (it's what 
		# required by this call)
		tmpVal = list(value) if type(value) == bytearray else value
		self.i2cbus.write_i2c_block_data(address, commandCode, tmpVal)

	#-----------------------------------------------------------------------
	# scan()
	#
	# Scans the I2C bus and returns a list of addresses that have a devices connected
	#
	@classmethod
	def scan(cls):
		""" Returns a list of addresses for the devices connected to the I2C bus."""
	
		# The plan - loop through the I2C address space and read a byte. If an 
		# OSError occures, a device isn't at that address. 
	
		if cls._i2cbus == None:
			cls._i2cbus = _connectToI2CBus()
	
		if cls._i2cbus == None:
			return []
	
		foundDevices = []
	
		# Loop over the address space - which is 7 bits (0-127 range)
		for currAddress in range(0, 128):
			try:
				cls._i2cbus.read_byte(currAddress)
			except Exception:
				continue
	
			foundDevices.append(currAddress)
	
	
		return foundDevices


