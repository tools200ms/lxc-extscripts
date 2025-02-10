import os

from lxcext.core.operations.abc_operation import Operation
from lxcext.core.runner.Pretender import RunPretend


class Mount(Operation):

    def start(self):
        name = self._opt_run['name']
        debug = self._opt_run['debug']
        pretend = True

        mount_dir = f"/mnt/lxc/{name}"

        print(f"Unmounting container: {name}")
        # Step 1: Unmount the filesystem
        RunPretend.run_command(f"umount {mount_dir}", debug=debug, pretend=pretend)

        # Step 2: Start the container
        RunPretend.run_command(f"lxc-start -n {name}", debug=debug, pretend=pretend)
        RunPretend.run_command(f"lxc-wait -n {name} -s RUNNING", debug=debug, pretend=pretend)

        print(f"Container {name} unmounted and restarted.")


def verify_integrity(self):
        pass
