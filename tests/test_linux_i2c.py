"""Linux bus selection without accessing I2C hardware."""
import unittest
from unittest.mock import patch

import qwiic_i2c
from qwiic_i2c.linux_i2c import LinuxI2C


class BusSelectionTests(unittest.TestCase):
    def test_explicit_bus_skips_detection(self):
        for bus in (0, 1, 3):
            with self.subTest(bus=bus), patch('smbus2.SMBus') as smbus, patch(
                'qwiic_i2c.linux_i2c._get_i2c_bus_id'
            ) as detect:
                driver = LinuxI2C(iBus=bus)
                smbus.assert_called_once_with(bus)
                detect.assert_not_called()
                self.assertIs(driver.i2cbus, smbus.return_value)

    def test_default_bus_is_detected(self):
        for board, bus in [('Raspberry Pi 4 Model B', 1), ('Jetson Orin Nano', 7)]:
            with self.subTest(board=board), patch('smbus2.SMBus') as smbus, patch(
                'qwiic_i2c.linux_i2c._get_board_name', return_value=board
            ):
                LinuxI2C()
                smbus.assert_called_once_with(bus)

    def test_factory_forwards_explicit_bus(self):
        with patch('smbus2.SMBus') as smbus, patch.object(
            qwiic_i2c, '_drivers', [LinuxI2C]
        ), patch.object(LinuxI2C, 'isPlatform', return_value=True):
            qwiic_i2c.get_i2c_driver(iBus=3)
            smbus.assert_called_once_with(3)
