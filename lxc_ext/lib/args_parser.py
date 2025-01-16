import argparse


class ArgsParser:

    @staticmethod
    def _add_common_arguments(create_parser):
        create_parser.add_argument("--config", default="lxcext.conf", help="Configuration file")
        create_parser.add_argument("--debug", action="store_true", help="Enable debug output")
        create_parser.add_argument("--pretend", "-p", action="store_true", help="Print commands without executing")

    @staticmethod
    def getArguments() -> {}:
        parser = argparse.ArgumentParser(description="LXC Container Management Tool")
        subparsers = parser.add_subparsers(dest="command")

        # Create container command
        create_parser = subparsers.add_parser("create", help="Create a new LXC container")
        create_parser.add_argument("name", help="Name of the container")
        create_parser.add_argument("--ip_address", help="IP address for the container")
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

        return parser.parse_args().__dict__
