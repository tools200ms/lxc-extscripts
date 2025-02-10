import os

from lxcext.core.operations.abc_operation import Operation
from lxcext.core.runner.Pretender import RunPretend


class Create(Operation):

    def start(self):
        name = self._opt_run['name']
        ip_addr = self._opt_run['ip_address']
        debug = self._opt_run['debug']
        pretend = True

        vgname = self._opt_srv['vgname']
        fssize = self._opt_srv['fssize']
        dist = self._opt_srv['dist']
        release = self._opt_srv['release']
        arch = self._opt_srv['arch']

        gateway = self._opt_net['gateway']


        print(f"Creating container: {name}")

        # Step 1: Create the container
        command = (
            f"lxc-create -n {name} -B lvm --lvname {name} --vgname {vgname} --fssize {fssize} "
            f"-f /etc/lxc/server.conf -t download -- -d {dist} -r {release} -a {arch}"
        )

        RunPretend.run_command(command, debug=debug, pretend=pretend)

        # Step 2: Configure networking
        config_path = "/dev/stdout"
            # f"/var/lib/lxc/{name}/config"
        with open(config_path, "a") as config_file:
            config_file.write(f"\n# Container specific network configuration:\n")
            config_file.write(f"lxc.net.0.ipv4.address = {ip_addr}\n")
            config_file.write(f"lxc.net.0.ipv4.gateway = {gateway}\n")

        # Step 3: Mount the filesystem
        mount_dir = f"/mnt/lxc/{name}"
        dev_path = f"/dev/mapper/{vgname}-" + name.replace("-", "--")
        os.makedirs(mount_dir, exist_ok=True)
        RunPretend.run_command(f"mount {dev_path} {mount_dir}", debug=debug, pretend=pretend)

        # Step 4: Copy necessary files and unmount
        RunPretend.run_command(f"cp -a /etc/resolv.conf {mount_dir}/etc/", debug=debug, pretend=pretend)
        # Alter: f"/etc/hostname" ?
        RunPretend.run_command(f"umount {mount_dir}", debug=debug, pretend=pretend)

        # Step 5: Start the container
        RunPretend.run_command(f"lxc-start -n {name}", debug=debug, pretend=pretend)
        RunPretend.run_command(f"lxc-wait -n {name} -s RUNNING", debug=debug, pretend=pretend)

        print(f"Container {name} created and started successfully.")

        # create user

    def verify_integrity(self):
        pass
