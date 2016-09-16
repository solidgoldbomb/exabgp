# encoding: utf-8
"""

Support for draft-hares-idr-common-header-00

Copyright (c) 2016 Job Snijders <job@ntt.net>
Copyright (c) 2009-2015 Exa Networks. All rights reserved.
"""

from exabgp.bgp.message.update.attribute import Attribute

from struct import pack
from struct import unpack

class CommonHeader (Attribute):
	MAX = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

	cache = {}
	caching = True

	__slots__ = ['common_header','_str']

	def __init__ (self, common_header):
		self.common_header = common_header
        self._str = "%d:%d:%d" % unpack('!HHL', self.common_header)

	def __eq__ (self, other):
		return self.common_header == other.common_header

	def json (self):
		self.ctype, self.length, self.global_admin = \
			unpack('!HHL', self.common_header)

		return """{ "type": %d, "length:" %d, "global_administrator": %d }""" % \
			(self.ctype, self.length, self.global_admin)

	def pack (self, negotiated=None):
		return self.common_header

	def __repr__ (self):
		return self._str

	def __len__ (self):
		return 12

	@classmethod
	def unpack (cls, common_header, negotiated):
		return cls(common_header)

	@classmethod
	def cached (cls, common_header):
		if cls.caching and common_header in cls.cache:
			return cls.cache[common_header]
		instance = cls(common_header)
		if cls.caching:
			cls.cache[common_header] = instance
		return instance
