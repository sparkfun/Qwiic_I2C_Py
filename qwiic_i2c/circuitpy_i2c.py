#-----------------------------------------------------------------------------
# cirucitpy_i2c.py
#
# Encapsulate CircuitPython I2C interface
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
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


# Import items from __future__ ? 
#  NO: There is no future with cicuit py

from .i2c_driver import I2CDriver

import sys
import os


_PLATFORM_NAME = "CircuitPython"

#-----------------------------------------------------------------------------
# Internal function to connect to the systems I2C bus.
#
# Attempts to fail elegantly. Put this in a central place to support 
# error handling  -- especially on non-circuitpy platforms
#
def _connectToI2CBus():

	try:
		import board
		import busio
	except Exception as ee:
		print("Error: Unable to load the I2C subsystem modules")
		return None

	daBus = None

	error=False

	# Connect - catch errors 

	try:
		daBus =  busio.I2C(board.SCL, board.SDA)
	except Exception as ee:
		if type(ee) is RuntimeError:
			print("Error:\tUnable to connect to I2C bus. %s" % (ee))
			print("\t\tEnsure a board is connected to the %s board." % (os.uname().machine))			
		else:
			print("Error:\tFailed to connect to I2C bus. Error: %s" % (ee))

		# We had an error.... 
		error=True

	# below is probably not needed, but ...
	if(not error and daBus == None):
		print("Error: Failed to connect to I2C bus. Unable to continue")

	return daBus


# notes on determining CirPy platform
#
# - os.uname().sysname == samd*
#
# 
class CircuitPythonI2C(I2CDriver):

	# Constructor
	name = _PLATFORM_NAME

	_i2cbus = None

	def __init__(self):

		# Call the super class. The super calss will use default values if not 
		# proviced
		I2CDriver.__init__(self)



	# Okay, are we running on a circuit py system?
	@classmethod
	def isPlatform(cls):

		# circuit py is mostly - for our purposes - on the samd21 or samd51 based boards
		return os.uname().sysname in ('samd21', 'samd51')


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

	#----------------------------------------------------------
	# read Data Command

	def readWord(self, address, commandCode):

		if not self.i2cbus.try_lock():
			return None

		self.i2cbus.writeto(address, commandCode, stop=False)

		buffer = bytearray(2)

		self.i2cbus.readfrom_into(address, buffer)

		# build and return a word
		return (buffer[1] << 8 ) | buffer[0]

	#----------------------------------------------------------
	def readByte(self, address, commandCode):

		if not self.i2cbus.try_lock():
			return None

		self.i2cbus.writeto(address, commandCode, stop=False)

		buffer = bytearray(1)

		self.i2cbus.readfrom_into(address, buffer)

		return buffer

	#----------------------------------------------------------
	def readBlock(self, address, commandCode, nBytes):

		if not self.i2cbus.try_lock():
			return None

		self.i2cbus.writeto(address, commandCode, stop=False)

		buffer = bytearray(nBytes)

		self.i2cbus.readfrom_into(address, buffer)

		return buffer

		
	#--------------------------------------------------------------------------	
	# write Data Commands 
	#
	# Send a command to the I2C bus for this device. 
	#
	# value = 16 bits of valid data..
	#

	def writeCommand(self, address, commandCode):

		if not self.i2cbus.try_lock():
			return None

		self.i2cbus.writeto(address, commandCode, stop=True)

	#----------------------------------------------------------
	def writeWord(self, address, commandCode, value):


		if not self.i2cbus.try_lock():
			return None

		self.i2cbus.writeto(address, commandCode, stop=False)
		buffer = bytearray(2)
		buffer[0] = value & 0xFF
		buffer[1] = (value >> 8) & 0xFF

		self.i2cbus.writeto(address, buffer, stop=True)		


	#----------------------------------------------------------
	def writeByte(self, address, commandCode, value):

		if not self.i2cbus.try_lock():
			return None

		self.i2cbus.writeto(address, commandCode, stop=False)
		self.i2cbus.writeto(address, bytes(value), stop=True)		

	#----------------------------------------------------------
	def writeBlock(self, address, commandCode, value):

		if not self.i2cbus.try_lock():
			return None

		self.i2cbus.writeto(address, commandCode, stop=False)

		data = [value] if isinstance(value, list) else value

		self.i2cbus.writeto(address, data, stop=True)


	#-----------------------------------------------------------------------
	# scan()
	#
	# Scans the I2C bus and returns a list of addresses that have a devices connected
	#
	@classmethod
	def scan(cls):
		""" Returns a list of addresses for the devices connected to the I2C bus."""
	
		# Just call the system build it....
	
		if cls._i2cbus == None:
			cls._i2cbus = _connectToI2CBus()
	
		if cls._i2cbus == None:
			return []
	
		if cls._i2cbus.try_lock():
			return cls._i2cbus.scan()
		else:
			return []



