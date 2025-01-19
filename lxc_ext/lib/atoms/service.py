from ast import Bytes

from lxc_ext.lib.atoms.atom import Atom


class fssize(Atom):
    def get(value: str) -> object:
        """
        Parses a string representing a size with units and converts it to bytes.

        Supported formats:
            - <number>M, <number>MB, <number> MB
            - <number>G, <number>GB, <number> GB
            - <number>MiB, <number> MiB
            - <number>GiB, <number> GiB
        Units can be in lowercase or uppercase.

        Args:
            value (str): The input size string.

        Returns:
            int: The size in bytes.

        Raises:
            ValueError: If the input string is not in a recognized format.
        """
        # Trim and normalize the input
        value = value.strip().lower()

        # Define unit multipliers
        unit_multipliers = {
            "m": 10 ** 6,
            "mb": 10 ** 6,
            "g": 10 ** 9,
            "gb": 10 ** 9,
            "mib": 2 ** 20,
            "gib": 2 ** 30,
        }

        # Extract the numeric part and unit
        import re
        match = re.match(r"^(\d+)\s*(\w+)?$", value)
        if not match:
            raise ValueError(f"Invalid size format: {value}")

        number, unit = match.groups()
        number = int(number)

        # Default to bytes if no unit is specified
        if unit is None:
            raise ValueError(f"Incorrect unit: {unit}, provide M, MB, MiB, G, GB, GiB")

        # Check if the unit is valid and get the multiplier
        if unit not in unit_multipliers:
            raise ValueError(f"Unrecognized unit: {unit}")

        multiplier = unit_multipliers[unit]
        # TODO: add type
        return round((number * multiplier) / 2 ** 20)

class dist:
    def get(value: str) -> object:
        return value

class release:
    def get(value: str) -> object:
        return value

class arch:
    def get(value: str) -> object:
        return value

class vgname:
    def get(value: str) -> object:
        return value

