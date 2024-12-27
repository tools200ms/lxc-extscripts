import os
import subprocess
import argparse
import configparser

# Load configuration
def load_config(config_file="lxc_ext.conf"):
    """Load configuration from a file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

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
    """Create a new LXC container with the specified parameters."""
    config = load_config(config_file)

    fssize = config.get("create", "fssize", fallback="2G")
    dist = config.get("create", "dist", fallback="devuan")
    release = config.get("create", "release", fallback="daedalus")
    arch = config.get("create", "arch", fallback="amd64")
    vgname = config.get("create", "vgname", fallback="vg0")

    print(f"Creating container: {name}")

    # Step 1: Create the container
    command = (
        f"lxc-create -n {name} -B lvm --lvname {name} --vgname {vgname} --fssize {fssize} "
        f"-f /etc/lxc/server.conf -t download -- -d {dist} -r {release} -a {arch}"
    )
    run_command(command, debug=debug, pretend=pretend)

    # Step 2: Configure networking
    config_path = f"/var/lib/lxc/{name}/config"
    with open(config_path, "a") as config_file:
        config_file.write(f"\n# Container specific network configuration:\n")
        config_file.write(f"lxc.net.0.ipv4.address = {ip_address}\n")
        config_file.write(f"lxc.net.0.ipv4.gateway = {gateway}\n")

    # Step 3: Mount the filesystem
    mount_dir = f"/mnt/lxc/{name}"
    dev_path = f"/dev/mapper/{vgname}-" + name.replace("-", "--")
    os.makedirs(mount_dir, exist_ok=True)
    run_command(f"mount {dev_path} {mount_dir}", debug=debug, pretend=pretend)

    # Step 4: Copy necessary files and unmount
    run_command(f"cp -a /etc/resolv.conf {mount_dir}/etc/", debug=debug, pretend=pretend)
    run_command(f"umount {mount_dir}", debug=debug, pretend=pretend)

    # Step 5: Start the container
    run_command(f"lxc-start -n {name}", debug=debug, pretend=pretend)
    run_command(f"lxc-wait -n {name} -s RUNNING", debug=debug, pretend=pretend)

    print(f"Container {name} created and started successfully.")

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
    parser = argparse.ArgumentParser(description="LXC Container Management Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Create container command
    create_parser = subparsers.add_parser("create", help="Create a new LXC container")
    create_parser.add_argument("name", help="Name of the container")
    create_parser.add_argument("ip_address", help="IP address for the container")
    create_parser.add_argument("gateway", help="Gateway for the container")
    create_parser.add_argument("--config", default="lxc_ext.conf", help="Configuration file")
    create_parser.add_argument("--debug", action="store_true", help="Enable debug output")
    create_parser.add_argument("--pretend", "-p", action="store_true", help="Print commands without executing")

    # Expand container command
    expand_parser = subparsers.add_parser("expand", help="Expand an LXC container filesystem")
    expand_parser.add_argument("name", help="Name of the container")
    expand_parser.add_argument("increment", help="Size increment (e.g., 2G)")
    expand_parser.add_argument("--config", default="lxc_ext.conf", help="Configuration file")
    expand_parser.add_argument("--debug", action="store_true", help="Enable debug output")
    expand_parser.add_argument("--pretend", "-p", action="store_true", help="Print commands without executing")

    # Mount/Unmount container command
    mount_parser = subparsers.add_parser("mount", help="Mount or unmount an LXC container filesystem")
    mount_parser.add_argument("name", help="Name of the container")
    mount_parser.add_argument("action", choices=["mount", "unmount"], help="Action to perform (mount or unmount)")
    mount_parser.add_argument("--config", default="lxc_ext.conf", help="Configuration file")
    mount_parser.add_argument("--debug", action="store_true", help="Enable debug output")
    mount_parser.add_argument("--pretend", "-p", action="store_true", help="Print commands without executing")

    args = parser.parse_args()

    if args.command == "create":
        create_container(
            name=args.name,
            ip_address=args.ip_address,
            gateway=args.gateway,
            config_file=args.config,
            debug=args.debug,
            pretend=args.pretend
        )
    elif args.command == "expand":
        expand_container(
            name=args.name,
            increment=args.increment,
            config_file=args.config,
            debug=args.debug,
            pretend=args.pretend
        )
    elif args.command == "mount":
        mount_container(
            name=args.name,
            action=args.action,
            config_file=args.config,
            debug=args.debug,
            pretend=args.pretend
        )
