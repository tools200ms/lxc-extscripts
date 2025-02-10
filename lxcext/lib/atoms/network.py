import ipaddress

from lxcext.core.IpAssingMethods import IpAssignRandom
from lxcext.lib.atoms.atom import Atom
from lxcext.lib.atoms.factory import Factory


class gateway(Atom):
    get = Factory.getIp

class ip_range(Atom):
    @staticmethod
    def get(value: str) -> object:
        if '-' not in value:
            return ipaddress.ip_network(value, strict=False)

        # Split the range into start and end IP addresses
        start_ip, end_ip = value.split('-')
        start_ip_obj = ipaddress.ip_address(start_ip.strip())
        end_ip_obj = ipaddress.ip_address(end_ip.strip())

        # Ensure both addresses are of the same type (IPv4 or IPv6)
        if type(start_ip_obj) is not type(end_ip_obj):
            raise ValueError("Start and end IP addresses must be of the same type.")

        # Validate that the start IP is less than or equal to the end IP
        if start_ip_obj > end_ip_obj:
            raise ValueError("Start IP must be less than or equal to the end IP.")

        return (start_ip_obj, end_ip_obj)

class ip_assign_method(Atom):
    def get(value: str) -> object:
        match value.lower():
            case "random":
                return IpAssignRandom

        raise Exception(f"Invalid value: {str}")

