import os
import subprocess




CONFIG = load_config()

# Utility functions
def run_command(command, debug=False, pretend=False):
    """Run a shell command and print debug information if enabled."""
    if debug or pretend:
        print(f"[DEBUG] Command: {command}")
    if not pretend:
        subprocess.run(command, shell=True, check=True)

# Module for creating LXC containers
def create_container(name, ip_address, gateway, config_file="lxc_ext.conf", debug=False, pretend=False):


# Module for expanding LXC container filesystem
def expand_container(name, increment, config_file="lxc_ext.conf", debug=False, pretend=False):
    """Expand the filesystem size of an LXC container."""
    config = load_config(config_file)
    vgname = config.get("expand", "vgname", fallback="vg0")

    print(f"Expanding container: {name} by {increment}")

    # Step 1: Stop the container if running
    run_command(f"lxc-stop -n {name}", debug=debug, pretend=pretend)
    run_command(f"lxc-wait -n {name} -s STOPPED", debug=debug, pretend=pretend)

    # Step 2: Resize the logical volume
    lv_path = f"/dev/{vgname}/{name}"
    run_command(f"lvextend -L+{increment} {lv_path}", debug=debug, pretend=pretend)

    # Step 3: Resize the filesystem
    run_command(f"resize2fs {lv_path}", debug=debug, pretend=pretend)

    # Step 4: Start the container
    run_command(f"lxc-start -n {name}", debug=debug, pretend=pretend)
    run_command(f"lxc-wait -n {name} -s RUNNING", debug=debug, pretend=pretend)

    print(f"Container {name} expanded by {increment} successfully.")

# Module for mounting and unmounting LXC container filesystem
def mount_container(name, action, config_file="lxc_ext.conf", debug=False, pretend=False):
    """Mount or unmount the filesystem of an LXC container."""
    config = load_config(config_file)
    vgname = config.get("mount", "vgname", fallback="vg0")

    mount_dir = f"/mnt/lxc/{name}"
    dev_path = f"/dev/mapper/{vgname}-" + name.replace("-", "--")

    if action == "mount":
        print(f"Mounting container: {name}")
        # Step 1: Stop the container if running
        run_command(f"lxc-stop -n {name}", debug=debug, pretend=pretend)
        run_command(f"lxc-wait -n {name} -s STOPPED", debug=debug, pretend=pretend)

        # Step 2: Mount the filesystem
        os.makedirs(mount_dir, exist_ok=True)
        run_command(f"mount {dev_path} {mount_dir}", debug=debug, pretend=pretend)

        print(f"Container {name} mounted at {mount_dir}.")

    elif action == "unmount":
        print(f"Unmounting container: {name}")
        # Step 1: Unmount the filesystem
        run_command(f"umount {mount_dir}", debug=debug, pretend=pretend)

        # Step 2: Start the container
        run_command(f"lxc-start -n {name}", debug=debug, pretend=pretend)
        run_command(f"lxc-wait -n {name} -s RUNNING", debug=debug, pretend=pretend)

        print(f"Container {name} unmounted and restarted.")

if __name__ == "__main__":

    args = parser.parse_args()

    if args.command == "create":

    elif args.command == "expand":
        expand_container(
            name        = args.name,
            increment   = args.increment,
            config_file = args.config,
            debug       = args.debug,
            pretend     = args.pretend
        )
    elif args.command == "mount":
        mount_container(
            name        = args.name,
            action      = args.action,
            config_file = args.config,
            debug       = args.debug,
            pretend     = args.pretend
        )
