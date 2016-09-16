# encoding: utf-8
"""

Support for draft-hares-idr-common-header-00

Copyright (c) 2016 Job Snijders <job@ntt.net>
Copyright (c) 2009-2015 Exa Networks. All rights reserved.
"""

from exabgp.bgp.message.update.attribute import Attribute

from struct import pack
from struct import unpack

"""

Header looks like:

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |            Type               |          Length               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                       Global Administrator                    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Types:

   Name                       Type Value      Transitivity
   ----                       ----------      ------------
   Reserved                   0x0000          n/a
   IETF Consensus             0x0001-0x02AA   Transitive
   IETF Consensus             0x02AB-0x0555   Non-Transitive
   First come First served    0x0556-0x07FF   Transitive
   First come First served    0x0800-0x0AAA   Non-Transitive
   Experimental use           0x0AAB-0x0FFF   Non-Transitive
   Reserved                   0x1000-0xFFFF   n/a

Currently only one type is needed for interop: 0x0001 (Large BGP Communities).

"""

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

    def _ctype (self, transitive=True):
        return pack(
            '!HHL',
            self.COMMUNITY_TYPE if transitive else self.COMMUNITY_TYPE | self.NON_TRANSITIVE,
            self.COMMUNITY_SUBTYPE
        )

	def __repr__ (self):
		h = 0x00
        for byte in self.common_header:
            h <<= 8
            h += ord(byte)
        return "0x%016X" % h

	def __len__ (self):
		return 16

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
