"""Test Python-openflow network types."""
import unittest

from pyof.foundation.basic_types import BinaryData
from pyof.foundation.network_types import VLAN, Ethernet, GenericTLV, IPv4


class TestNetworkTypes(unittest.TestCase):
    """Reproduce bugs found."""

    def test_GenTLV_value_unpack(self):
        """Value attribute should be the same after unpacking."""
        value = BinaryData(b'test')
        tlv = GenericTLV(value=value)
        tlv_unpacked = GenericTLV()
        tlv_unpacked.unpack(tlv.pack())
        self.assertEqual(tlv.value.value, tlv_unpacked.value.value)


class TestEthernet(unittest.TestCase):
    """Test Ethernet frames."""

    def test_Ethernet_pack(self):
        """Test pack method of Ethernet class without VLAN tag."""
        ethernet = Ethernet(destination='00:1f:3a:3e:9a:cf',
                            source='00:15:af:d5:38:98', ether_type=0x800,
                            data=b'testdata')
        packed = ethernet.pack()
        expected = b'\x00\x1f:>\x9a\xcf\x00\x15\xaf\xd58\x98\x08\x00testdata'
        self.assertEqual(packed, expected)

    def test_Ethernet_unpack(self):
        """Test pack method of Ethernet class without VLAN tag."""
        raw = b'\x00\x15\xaf\xd58\x98\x00\x1f:>\x9a\xcf\x08\x00testdata'
        expected = Ethernet(destination='00:15:af:d5:38:98',
                            source='00:1f:3a:3e:9a:cf', ether_type=0x800,
                            data=b'testdata')
        expected.pack()
        unpacked = Ethernet()
        unpacked.unpack(raw)
        self.assertEqual(unpacked, expected)

    def test_Tagged_Ethernet_pack(self):
        """Test pack method of Ethernet class including VLAN tag."""
        ethernet = Ethernet(destination='00:1f:3a:3e:9a:cf',
                            source='00:15:af:d5:38:98', vlan=VLAN(vid=200),
                            ether_type=0x800, data=b'testdata')
        packed = ethernet.pack()
        expected = b'\x00\x1f:>\x9a\xcf\x00\x15\xaf\xd58'
        expected += b'\x98\x81\x00\x00\xc8\x08\x00testdata'
        self.assertEqual(packed, expected)

    def test_Tagged_Ethernet_unpack(self):
        """Test pack method of Ethernet class including VLAN tag."""
        raw = b'\x00\x15\xaf\xd58\x98\x00\x1f:>'
        raw += b'\x9a\xcf\x81\x00!^\x08\x00testdata'
        expected = Ethernet(destination='00:15:af:d5:38:98',
                            source='00:1f:3a:3e:9a:cf', vlan=VLAN(pcp=1,
                                                                  vid=350),
                            ether_type=0x800, data=b'testdata')
        expected.pack()
        unpacked = Ethernet()
        unpacked.unpack(raw)
        self.assertEqual(unpacked, expected)


class TestVLAN(unittest.TestCase):
    """Test VLAN headers."""

    def test_VLAN_pack(self):
        """Test pack method of VLAN class."""
        vlan = VLAN(pcp=3, vid=20)
        packed = vlan.pack()
        expected = b'\x81\x00`\x14'
        self.assertEqual(packed, expected)

    def test_VLAN_unpack(self):
        """Test unpack method of VLAN class."""
        raw = b'\x81\x00\xa0{'
        expected = VLAN(pcp=5, vid=123)
        unpacked = VLAN()
        unpacked.unpack(raw)
        self.assertEqual(unpacked, expected)


class TestIPv4(unittest.TestCase):
    """Test IPv4 packets."""

    def test_IPv4_pack(self):
        """Test pack/unpack of IPv4 class."""
        packet = IPv4(dscp=10, ttl=64, protocol=17, source="192.168.0.10",
                      destination="172.16.10.30", options=b'1000',
                      data=b'testdata')
        packed = packet.pack()
        expected = b'F(\x00 \x00\x00\x00\x00@\x11\x02'
        expected += b'\xc5\xc0\xa8\x00\n\xac\x10\n\x1e1000testdata'
        self.assertEqual(packed, expected)

    def test_IPv4_unpack(self):
        """Test unpack of IPv4 binary packet."""
        raw = b'FP\x00$\x00\x00\x00\x00\x80\x06W'
        raw += b'\xf4\n\x9aN\x81\xc0\xa8\xc7\xcc1000somemoredata'
        expected = IPv4(dscp=20, ttl=128, protocol=6, source="10.154.78.129",
                        destination="192.168.199.204", options=b'1000',
                        data=b'somemoredata')
        expected.pack()
        unpacked = IPv4()
        unpacked.unpack(raw)
        self.assertEqual(unpacked, expected)

    def test_IPv4_size(self):
        """Test Header size for IPv4 packet."""
        packet = IPv4()
        packet.pack()
        self.assertEqual(20, packet.get_size())
        self.assertEqual(20, packet.length)
        self.assertEqual(20, packet.ihl * 4)

    def test_IPv4_checksum(self):
        """Test if the IPv4 checksum is being calculated correclty."""
        packet = IPv4(dscp=10, ttl=64, protocol=17, source="192.168.0.10",
                      destination="172.16.10.30", options=b'1000',
                      data=b'testdata')
        packet.pack()
        self.assertEqual(packet.checksum, 709)
