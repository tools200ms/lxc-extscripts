
from abc import ABC, abstractmethod


class Operation(ABC):
    def __init__(self, options: {}):
        self._opt = options
        self._opt_run = options['run']
        self._opt_srv = options['service']
        self._opt_net = options['network']

    @abstractmethod
    def start(self): pass
    @abstractmethod
    def verify_integrity(self): pass

    @staticmethod
    def getOperation(options: {}):
        """
        Returns the constructor of the non-abstract subclass of Operation matching the name (case-insensitive).

        """
        name = options['run']['command'].lower()

        match name:
            case "create":
                from lxcext.core.operations.create import Create
                return Create(options)
            case "expand":
                from lxcext.core.operations.expand import Expand
                return Expand(options)
            case "mount":
                from lxcext.core.operations.mount import Mount
                return Mount(options)

        # If no matching class is found, raise an exception
        raise ValueError(f"Unknown operation: '{name}'.")

