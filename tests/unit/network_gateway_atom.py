import unittest
import ipaddress

from lxcext.lib.atoms.network import gateway


class TestParseIpAddress(unittest.TestCase):

    def test_valid_ipv4(self):
        result = gateway.get("192.168.1.1")
        self.assertIsInstance(result, ipaddress.IPv4Address)
        self.assertEqual(str(result), "192.168.1.1")

    def test_valid_ipv6(self):
        result = gateway.get("2001:db8::1")
        self.assertIsInstance(result, ipaddress.IPv6Address)
        self.assertEqual(str(result), "2001:db8::1")

    def test_invalid_ip(self):
        with self.assertRaises(ValueError):
            gateway.get("invalid_ip")

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            gateway.get("")

    #def test_valid_ipv4_with_leading_zeros(self):
    #    result = gateway.get("192.168.001.001")
    #    self.assertIsInstance(result, ipaddress.IPv4Address)
    #    self.assertEqual(str(result), "192.168.1.1")

    def test_valid_ipv6_with_uppercase(self):
        result = gateway.get("2001:DB8::1")
        self.assertIsInstance(result, ipaddress.IPv6Address)
        self.assertEqual(str(result), "2001:db8::1")

if __name__ == '__main__':
    unittest.main()
