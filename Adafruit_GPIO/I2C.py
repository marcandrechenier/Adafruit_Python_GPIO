# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
# Based on Adafruit_I2C.py created by Kevin Townsend.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging

import smbus


logger = logging.getLogger(__name__)


def reverseByteOrder(data):
	"""Reverses the byte order of an int (16-bit) or long (32-bit) value."""
	# Courtesy Vishal Sapre
	byteCount = len(hex(data)[2:].replace('L','')[::2])
	val       = 0
	for i in range(byteCount):
		val    = (val << 8) | (data & 0xff)
		data >>= 8
	return val

def get_default_bus():
	"""Return the default bus number based on the device platform.  For a
	Raspberry Pi either bus 0 or 1 (baed on the Pi revision) will be returned.
	For a Beaglebone Black the first user accessible bus, 1, will be returned.
	"""
	return 0


class Device(object):
	"""Class for communicating with an I2C device using the smbus library.
	Allows reading and writing 8-bit, 16-bit, and byte array values to registers
	on the device."""
	logger = logging.getLogger(__name__)
	def __init__(self, address, busnum):
		"""Create an instance of the I2C device at the specified address on the
		specified I2C bus number."""
		self._address = address
		self._bus = smbus.SMBus(busnum)
		self._logger = logging.getLogger('Adafruit_I2C.Device.Bus.{0}.Address.{1:#0X}' \
								.format(busnum, address))

	def write8(self, register, value):
		"""Write an 8-bit value to the specified register."""
		value = value & 0xFF
		self._bus.write_byte_data(self._address, register, value)
		self._logger.debug("Wrote 0x%02X to register 0x%02X", 
					 value, register)

	def write16(self, register, value):
		"""Write a 16-bit value to the specified register."""
		value = value & 0xFFFF
		self._bus.write_word_data(self._address, register, value)
		self._logger.debug("Wrote 0x%04X to register pair 0x%02X, 0x%02X", 
					 value, register, register+1)

	def writeList(self, register, data):
		"""Write bytes to the specified register."""
		self._bus.write_i2c_block_data(self._address, register, data)
		self._logger.debug("Wrote to register 0x%02X: %s", 
					 register, data)

	def readList(self, register, length):
		"""Read a length number of bytes from the specified register.  Results 
		will be returned as a bytearray."""
		results = self._bus.read_i2c_block_data(self._address, register, length)
		self._logger.debug("Read the following from register 0x%02X: %s",
			 		 register, results)
		return results

	def readU8(self, register):
		"""Read an unsigned byte from the specified register."""
		result = self._bus.read_byte_data(self._address, register) & 0xFF
		self._logger.debug("Read 0x%02X from register 0x%02X",
					 result, register)
		return result

	def readS8(self, register):
		"""Read a signed byte from the specified register."""
		result = self._bus.read_byte_data(self._address, register) & 0xFF
		if result > 127: 
			result -= 256
		self._logger.debug("Read 0x%02X from register 0x%02X",
					 result, register)
		return result

	def readU16(self, register):
		"""Read an unsigned 16-bit value from the specified register."""
		result = self._bus.read_word_data(self._address,register) & 0xFFFF
		self._logger.debug("Read 0x%04X from register pair 0x%02X, 0x%02X",
					 result, register, register+1)
		return result

	def readS16(self, register):
		"""Read a signed 16-bit value from the specified register."""
		result = self._bus.read_word_data(self._address,register)
		if result > 32767:
			result -= 65536
		self._logger.debug("Read 0x%04X from register pair 0x%02X, 0x%02X",
					 result, register, register+1)
		return result
