import ipaddress


class Factory:
    @staticmethod
    def getIp(value: str) -> object:
        try:
            # Attempt to create an IPv4 or IPv6 address object
            return ipaddress.ip_address(value)
        except ValueError:
            raise ValueError(f"'{value}' is not a valid IP address.")

