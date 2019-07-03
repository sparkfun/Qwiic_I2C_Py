#
#-----------------------------------------------------------------------------
# i2c_driver.py
#
# Base class used to define the interface for the platform classes. 
#
# A platform class performs the following:
#
#   - Determines if the object is executing on it's desired platform
#		- Platforms are strucutre into broad classifications. For example
#			- Linux systems
#			- CircuitPython 
#
#	- Implements platform specific logic to support a given operation (I2C for now)
#
# This specific class does very little besides define the base interface  
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------
"""
i2c_driver
============
This is an abstract class used to define the common I2C interface for the qwiic I2C 
implementation. Platform specific drivers sub-class this object and implement the 
neccessary methods.

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""

from __future__ import print_function


#-----------------------------------------------------------------------------
# Platform
#
# Base class to define the interface for our platform I2C driver
#
#
class I2CDriver(object):
	"""
	I2CDriver

		Implements the interface for the I2C bus for the qwiic ecosystem.

		:return: The I2C Driver interface for the qwiic system.
		:rtype: Object
	"""

	# stubs
	name = 'qwiic I2C abstract base class'

	def __init__(self):
		pass


	# A class method is used to determine if the system is executing on the desired platform

	@classmethod
	def isPlatform(cls):
		""" 
			Called to determine if the specific driver supports the current platorm

			:return: True if this platform is supported, otherwise False
			:rtype: bool

		"""
		pass


	#-------------------------------------------------------------------------	
	# stubs to support Python with statements. 
	#
	# Helpful for I2C interactions that require a mutex.

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		pass


	#-------------------------------------------------------------------------		
	# read Data Command

	def readWord(self, address, commandCode):
		""" 
			Called to read a word (16 bits) from a specific device.

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from 

			:return: Returns the read data
			:rtype: integer - first 16 bits contain the read data. 

		"""
		return None

	def readByte(self, address, commandCode):
		""" 
			Called to read a byte (8 bits) from a specific device.

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from 

			:return: Returns the read data
			:rtype: integer - first 8 bits contain the read data. 

		"""
		return None

	def readBlock(self, address, commandCode, nBytes):
		""" 
			Called to read a block of bytesfrom a specific device.

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from
			:param nBytes: The number of bytes to read from the device

			:return: Returns the read data as a list of integers.
			:rtype: list 

		"""
		return None
		
	#--------------------------------------------------------------------------	
	# write Data Commands 
	#
	# Send a command to the I2C bus for this device. 
	#
	# value = 16 bits of valid data..
	#

	def writeCommand(self, address, commandCode):
		""" 
			Called to write a command to a device. No actual data is written

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from 

			:return: None

		"""
		return None

	def writeWord(self, address, commandCode, value):
		""" 
			Called to write a word (16 bits) to a device. 

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from
			:param value: The word (16 bits) to write to the I2C bus

			:return: None

		"""

		return None


	def writeByte(self, address, commandCode, value):
		""" 
			Called to write a byte (8 bits) to a device. 

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from
			:param value: The byte (8 bits) to write to the I2C bus

			:return: None

		"""

		return None

	def writeBlock(self, address, commandCode, value):
		""" 
			Called to write a block of bytes to a device. 

			:param address: The I2C address of the device to read from
			:param commandCode: The "command" or register to read from
			:param value: A list of bytes (ints) to write on the I2C bus.

			:return: None

		"""
		pass

	@classmethod
	def scan(cls):
		"""
			Used to scan the I2C bus, returning a list of I2C address attached to the computer.

			:return: A list of I2C addresses. If no devices are attached, an empty list is returned.
			:rtype: list

		"""
		return None



