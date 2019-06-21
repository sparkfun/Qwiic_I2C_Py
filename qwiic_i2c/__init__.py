#-----------------------------------------------------------------------------
# __init__.py
#
#------------------------------------------------------------------------
#
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
#
#-----------------------------------------------------------------------------
# Package to abstract the interace to the execution platforms I2C bus for QWIIC.
#
#
#
#-----------------------------------------------------------------------------
# utility functions
from .i2c_driver 	import I2CDriver
from .linux_i2c 	import LinuxI2C
from .circuitpy_i2c import CircuitPythonI2C

_drivers = [LinuxI2C, CircuitPythonI2C]

_theDriver = None

# Exported method to get the I2C driver for the execution plaform. 
#
# If no driver is found, a None value is returne.d

def getI2CDriver():

	global _theDriver

	if _theDriver != None:
		return _theDriver

	

	for driverClass in _drivers:

		# Does this class/driverd support this platform?
		if driverClass.isPlatform():

			_theDriver = driverClass()
			# Yes - return the driver object
			return _theDriver

	return None

def isDeviceConnected(devAddress):

	i2c = getI2CDriver()

	if not i2c:
		print("Unable to load the I2C driver for this device")
		return False
	
	isConnected = False
	try:
		# Try to write a byte to the device, command 0x0
		# If it throws an I/O error - the device isn't connected
		with i2c as i2cDriver:
			i2cDriver.writeCommand(devAddress, 0x0)

			isConnected = True
	except Exception as ee:
		print("Error connecting to Device: %X, %s" % (devAddress, ee))
		pass

	return isConnected
