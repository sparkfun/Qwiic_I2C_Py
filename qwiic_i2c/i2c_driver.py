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
#			- MicroPlatform

#	- Implements platform specific logic to support a given operation (I2C for now)
#
# This specific class does very little besides define the base interface  
#
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
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------

from __future__ import print_function


#-----------------------------------------------------------------------------
# Platform
#
# Base class to define the interface for our platform I2C driver
#
#
class I2CDriver(object):


	# stubs
	name = 'qwiic I2C abstract base class'

	def __init__(self):
		pass


	# A class method is used to determine if the system is executing on the desired platform

	@classmethod
	def isPlatform(cls):
		pass


	#-------------------------------------------------------------------------	
	# stubs

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		pass


	#-------------------------------------------------------------------------		
	# read Data Command

	def readWord(self, address, commandCode):
		return None

	def readByte(self, address, commandCode):
		return None

	def readBlock(self, address, commandCode, nBytes):
		return None
		
	#--------------------------------------------------------------------------	
	# write Data Commands 
	#
	# Send a command to the I2C bus for this device. 
	#
	# value = 16 bits of valid data..
	#

	def writeCommand(self, address, commandCode):

		return None

	def writeWord(self, address, commandCode, value):

		return None


	def writeByte(self, address, commandCode, value):

		return None

	def writeBlock(self, address, commandCode, value):
		pass

	@classmethod
	def scan(cls):
		return None



