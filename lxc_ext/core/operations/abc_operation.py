import inspect
import sys
from abc import ABC, abstractmethod
from pprint import pprint


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
        name = name.lower()

        current_module = sys.modules[__name__]
        print(sys.modules[__name__])
        # Use inspect.getmembers to find classes
        classes = inspect.getmembers(current_module, inspect.isclass)

        # Filter classes that are defined in this module (not imported)
        local_classes = [cls_name for cls_name, cls_obj in classes if cls_obj.__module__ == __name__]


        # Get all subclasses of Operation
        subclasses = Operation.__subclasses__()

        pprint(local_classes)
        # Iterate through the subclasses to find a match
        for subclass in subclasses:
            print(subclass.__name__)
            if subclass.__name__.lower() == name:
                # Check if the class is non-abstract by inspecting __abstractmethods__
                if not getattr(subclass, "__abstractmethods__", False):
                    return subclass  # Return the class constructor

        # If no matching class is found, raise an exception
        raise ValueError(f"Unknown operation: '{name}'.")

