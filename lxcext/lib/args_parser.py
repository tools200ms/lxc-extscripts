import sys

from pprint import pprint

import argparse

from lxcext.core.operations.abc_operation import Operation
from lxcext.lib.atoms.args import Args
from lxcext.lib.atoms.factory import Factory
from lxcext.lib.conf_parser import ConfParser


class ArgsParser:

    class NonGeneralConfigArg:
        pass

    @staticmethod
    def _add_common_arguments(sub_parser):
        sub_parser.add_argument("--config", default="lxcext.conf", help="Configuration file")
        sub_parser.add_argument("--debug", action="store_true", help="Enable debug output")
        sub_parser.add_argument("--pretend", "-p", action="store_true", help="Print commands without executing")

    def __init__(self):
        parser = argparse.ArgumentParser(description="LXC Container Management Tool")

        subparsers = parser.add_subparsers(dest="command")

        # Create container command
        create_parser = subparsers.add_parser("create", help="Create a new LXC container")
        create_parser.add_argument("name", help="Name of the container")
        # class: server|client
        create_parser.add_argument("--ip_address", type=Factory.getIp, default=None, help="IP address for the container")
        create_parser.add_argument("--gateway", help="Gateway for the container")
        ArgsParser._add_common_arguments(create_parser)

        # Expand container command
        expand_parser = subparsers.add_parser("expand", help="Expand an LXC container filesystem")
        expand_parser.add_argument("name", help="Name of the container")
        expand_parser.add_argument("increment", help="Size increment (e.g., 2G)")
        ArgsParser._add_common_arguments(expand_parser)

        # Mount/Unmount container command
        mount_parser = subparsers.add_parser("mount", help="Mount or unmount an LXC container filesystem")
        mount_parser.add_argument("name", help="Name of the container")
        mount_parser.add_argument("action", choices=["mount", "unmount"], help="Action to perform (mount or unmount)")
        ArgsParser._add_common_arguments(mount_parser)

        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)

        self.__parser = parser
        self.__args = parser.parse_args()

    def getConfigFilePath(self) -> str:

        if 'config' in self.__args.__dict__:
            return self.__args.__dict__['config']

        return ConfParser.DEFAULT_PATH

    def merge(self, conf: {}) -> {}:
        final_conf = conf.copy()
        final_conf['run'] = {}
        filter = ['help']

        for ak, av in self.__args.__dict__.items():
            if ak in filter:
                continue

            #if av is ArgsParser.NonGeneralConfigArg:
            if not hasattr(Args, ak):
                final_conf['run'][ak] = av
                continue

            cls = getattr(Args, ak)
            mod_name = cls.__module__

            if mod_name.endswith('.service'):
                key_arr = final_conf['service']
            elif mod_name.endswith('.network'):
                key_arr = final_conf['network']
            else:
                raise Exception(f"Internall error: unsupported name: {mod_name}")

            if av is not None:
                # overwrite default value
                key_arr[ak] = av

        return final_conf

