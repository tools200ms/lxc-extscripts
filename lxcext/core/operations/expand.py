
from lxcext.core.operations.abc_operation import Operation
from lxcext.core.runner.Pretender import RunPretend


class Expand(Operation):

    def start(self):
        name = self._opt_run['name']
        debug = self._opt_run['debug']
        pretend = True

        vgname = self._opt_srv['vgname']
        fs_extr_size = self._opt_srv['increment']

        print(f"Expanding container: {name} by {fs_extr_size}")

        # Step 1: Stop the container if running
        RunPretend.run_command(f"lxc-stop -n {name}", debug=debug, pretend=pretend)
        RunPretend.run_command(f"lxc-wait -n {name} -s STOPPED", debug=debug, pretend=pretend)

        # Step 2: Resize the logical volume
        lv_path = f"/dev/{vgname}/{name}"
        RunPretend.run_command(f"lvextend -L+{fs_extr_size} {lv_path}", debug=debug, pretend=pretend)

        # Step 3: Resize the filesystem
        RunPretend.run_command(f"resize2fs {lv_path}", debug=debug, pretend=pretend)

        # Step 4: Start the container
        RunPretend.run_command(f"lxc-start -n {name}", debug=debug, pretend=pretend)
        RunPretend.run_command(f"lxc-wait -n {name} -s RUNNING", debug=debug, pretend=pretend)

        print(f"Container {name} expanded by {fs_extr_size} successfully.")

    def verify_integrity(self):
        pass
