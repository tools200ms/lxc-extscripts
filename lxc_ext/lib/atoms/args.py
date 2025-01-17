from lxc_ext.lib.atoms import service, network


class Args:
    # Some configuration file settings (commonly used) can be
    # overwritten with a command line arguments, below code
    # links what can be overwritten
    fssize = service.fssize
    vgname = service.vgname

    gateway = network.gateway
    ip_range = network.ip_range
    ip_assign_method = network.ip_assign_method

