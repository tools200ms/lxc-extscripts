from lxc_ext.core.IpAssingMethods import IpAssignRandom
from lxc_ext.lib.atoms.atom import Atom


class ip_assign(Atom):
    def get(value: str) -> object:
        match value.lower():
            case "random":
                return IpAssignRandom

        raise Exception(f"Invalid value: {str}")
