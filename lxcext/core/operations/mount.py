import os

from lxcext.core.operations.abc_operation import Operation
from lxcext.core.runner.Pretender import RunPretend


class Mount(Operation):

    def start(self):
        name = self._opt_run['name']
        debug = self._opt_run['debug']
        pretend = True

        vgname = self._opt_srv['vgname']

        mount_dir = f"/mnt/lxc/{name}"
        dev_path = f"/dev/mapper/{vgname}-" + name.replace("-", "--")

        print(f"Mounting container: {name}")
        # Step 1: Stop the container if running
        RunPretend.run_command(f"lxc-stop -n {name}", debug=debug, pretend=pretend)
        RunPretend.run_command(f"lxc-wait -n {name} -s STOPPED", debug=debug, pretend=pretend)

        # Step 2: Mount the filesystem
        os.makedirs(mount_dir, exist_ok=True)
        RunPretend.run_command(f"mount {dev_path} {mount_dir}", debug=debug, pretend=pretend)

        print(f"Container {name} mounted at {mount_dir}.")

    def verify_integrity(self):
        pass
