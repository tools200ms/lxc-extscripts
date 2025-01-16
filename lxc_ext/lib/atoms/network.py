import ipaddress

from lxc_ext.lib.atoms.atom import Atom


class gateway(Atom):
    @staticmethod
    def get(value: str) -> object:
        try:
            # Attempt to create an IPv4 or IPv6 address object
            return ipaddress.ip_address(value)
        except ValueError:
            raise ValueError(f"'{value}' is not a valid IP address.")

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
