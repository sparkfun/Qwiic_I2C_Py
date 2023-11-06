#-----------------------------------------------------------------------------
# micropython_i2c.py
#
# Encapsulate MicroPython port I2C interface
#------------------------------------------------------------------------
#
# Written by  oclyke, Feb 2021
# 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2021 SparkFun Electronics
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

from .i2c_driver import I2CDriver

import sys

_PLATFORM_NAME = "MicroPython"

# used internally in this file to get i2c class object 
def _connectToI2CBus(freq=400000):
	try:
		from machine import I2C, Pin
		if sys.platform == 'rp2':
			# Todo: Don't hard code I2C pin and port!
			return I2C(id=1, scl=Pin(19), sda=Pin(18), freq=freq)
		elif 'xbee' in sys.platform:
			return I2C(id=1, freq=freq)
		else:
			raise Exception("Unknown MicroPython platform: " + sys.platform)
	except Exception as e:
		print(str(e))
		print('error: failed to connect to i2c bus')
	return None

class MicroPythonI2C(I2CDriver):

	# Constructor
	name = _PLATFORM_NAME
	_i2cbus = None

	def __init__(self):
		I2CDriver.__init__(self) # init super

	@classmethod
	def isPlatform(cls):
		try:
			return 'micropython' in sys.implementation
		except:
			return False


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

		if(name != 'i2cbus'):
			super(I2CDriver, self).__setattr__(name, value)

	# read commands ----------------------------------------------------------
	def readWord(self, address, commandCode):
		buffer = self.i2cbus.readfrom_mem(address, commandCode, 2)
		return (buffer[1] << 8 ) | buffer[0]

	def readByte(self, address, commandCode):
		return self.i2cbus.readfrom_mem(address, commandCode, 1)[0]

	def readBlock(self, address, commandCode, nBytes):
		return self.i2cbus.readfrom_mem(address, commandCode, nBytes)

		
	# write commands----------------------------------------------------------
	def writeCommand(self, address, commandCode):
		self.i2cbus.writeto(address, commandCode.to_bytes(1, 'little'))

	def writeWord(self, address, commandCode, value):
		self.i2cbus.writeto_mem(address, commandCode, value.to_bytes(2, 'little'))

	def writeByte(self, address, commandCode, value):
		self.i2cbus.writeto_mem(address, commandCode, value.to_bytes(1, 'little'))

	def writeBlock(self, address, commandCode, value):
		self.i2cbus.writeto_mem(address, commandCode, bytes(value))


	# scan -------------------------------------------------------------------
	@classmethod
	def scan(cls):
		""" Returns a list of addresses for the devices connected to the I2C bus."""
	
		if cls._i2cbus == None:
			cls._i2cbus = _connectToI2CBus()
	
		if cls._i2cbus == None:
			return []
			
		return cls._i2cbus.scan()
