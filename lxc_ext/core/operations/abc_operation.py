
from abc import ABC, abstractmethod

from lxc_ext.lib.conf_parser import ConfParser


class Operation(ABC):
    def __init(args: (), self, conf: ()):
        self.__args = args
        self.__conf = conf

    @abstractmethod
    def start(self): pass
    @abstractmethod
    def verify_integrity(self): pass

    @staticmethod
    def getOperation(name: str):
        """
        Returns the constructor of the non-abstract subclass of Operation matching the name (case-insensitive).

        :param name: Name of the operation class to find (case-insensitive).
        :return: Reference to the constructor of the matching class.
        :raises ValueError: If no matching non-abstract subclass is found.
        """
        # Get all subclasses of Operation
        subclasses = Operation.__subclasses__()

        # Iterate through the subclasses to find a match
        for subclass in subclasses:
            if subclass.__name__.lower() == name.lower():
                # Check if the class is non-abstract by inspecting __abstractmethods__
                if not getattr(subclass, "__abstractmethods__", False):
                    return subclass  # Return the class constructor

        # If no matching class is found, raise an exception
        raise ValueError(f"No non-abstract subclass of Operation found for name '{name}'.")

