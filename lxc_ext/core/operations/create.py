from lxc_ext.core.operations.abc_operation import Operation


class Create(Operation):

    def start(self):
        pass
        """Create a new LXC container with the specified parameters."""
        # fssize = config.get("create", "fssize", fallback="2G")
        # dist = config.get("create", "dist", fallback="devuan")
        # release = config.get("create", "release", fallback="daedalus")
        # arch = config.get("create", "arch", fallback="amd64")
        # vgname = config.get("create", "vgname", fallback="vg0")
        #
        # print(f"Creating container: {name}")
        #
        # self.__args
        # Step 1: Create the container
        # command = (
        #     f"lxc-create -n {name} -B lvm --lvname {name} --vgname {vgname} --fssize {fssize} "
        #     f"-f /etc/lxc/server.conf -t download -- -d {dist} -r {release} -a {arch}"
        # )
        # run_command(command, debug=debug, pretend=pretend)
        #
        # # Step 2: Configure networking
        # config_path = f"/var/lib/lxc/{name}/config"
        # with open(config_path, "a") as config_file:
        #     config_file.write(f"\n# Container specific network configuration:\n")
        #     config_file.write(f"lxc.net.0.ipv4.address = {ip_address}\n")
        #     config_file.write(f"lxc.net.0.ipv4.gateway = {gateway}\n")
        #
        # # Step 3: Mount the filesystem
        # mount_dir = f"/mnt/lxc/{name}"
        # dev_path = f"/dev/mapper/{vgname}-" + name.replace("-", "--")
        # os.makedirs(mount_dir, exist_ok=True)
        # run_command(f"mount {dev_path} {mount_dir}", debug=debug, pretend=pretend)
        #
        # # Step 4: Copy necessary files and unmount
        # run_command(f"cp -a /etc/resolv.conf {mount_dir}/etc/", debug=debug, pretend=pretend)
        # run_command(f"umount {mount_dir}", debug=debug, pretend=pretend)
        #
        # # Step 5: Start the container
        # run_command(f"lxc-start -n {name}", debug=debug, pretend=pretend)
        # run_command(f"lxc-wait -n {name} -s RUNNING", debug=debug, pretend=pretend)
        #
        # print(f"Container {name} created and started successfully.")

    def verify_integrity(self):
        pass