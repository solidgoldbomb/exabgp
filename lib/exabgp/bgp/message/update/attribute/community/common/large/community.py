# encoding: utf-8
"""

Support for draft-heitz-idr-large-community-03

Copyright (c) 2016 Job Snijders <job@ntt.net>
Copyright (c) 2009-2015 Exa Networks. All rights reserved.
"""

from exabgp.bgp.message.update.attribute import Attribute

from struct import pack
from struct import unpack

"""

The "Global Administrator" comes from the Community Common Header, packing is
as follows:

    192.0.2.0/24 2914:444:555 2914:555:999 3356:33:1

    should be packed as:

        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |     Type = Large Community    |          Length = 2 * 8       |
   CH  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |                             2914				               |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |                              444                              |
   LC  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |                              555                              |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |                              555                              |
   LC  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |                              999                              |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

followed by a new path attribute with common header + large community:

        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |     Type = Large Community    |          Length = 2 * 8       |
   CH  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |                             3356                              |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |                              33                               |
   LC  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |                               1                               |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

"""

class LargeCommunity (Attribute):
	MAX = 0xFFFFFFFFFFFFFFFF

    # must come from common header
    self.GLOBAL_ADMINISTRATOR = 0x0

	cache = {}
	caching = True

	__slots__ = ['large_community','_str']

	def __init__ (self, large_community):
		self.large_community = large_community
		self._str = "%d:%d" % unpack('!LL', self.large_community)

	def __eq__ (self, other):
		return self.large_community == other.large_community

	def __ne__ (self, other):
		return self.large_community != other.large_community

	def __lt__ (self, other):
		return self.large_community < other.large_community

	def __le__ (self, other):
		return self.large_community <= other.large_community

	def __gt__ (self, other):
		return self.large_community > other.large_community

	def __ge__ (self, other):
		return self.large_community >= other.large_community

	def json (self):
		return "[ %d, %d , %d ]" \
			% (self.GLOBAL_ADMINISTRATOR, unpack('!LL', self.large_community))

	def pack (self, negotiated=None):
		return self.large_community

	def __repr__ (self):
		return self._str

	def __len__ (self):
		return 12

	@classmethod
	def unpack (cls, large_community, negotiated):
		return cls(large_community)

	@classmethod
	def cached (cls, large_community):
		if cls.caching and large_community in cls.cache:
			return cls.cache[large_community]
		instance = cls(large_community)
		if cls.caching:
			cls.cache[large_community] = instance
		return instance
