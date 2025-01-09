from pprint import pprint

from lxc_ext.core.operations.abc_operation import Operation
from lxc_ext.lib.args_parser import ArgsParser
from lxc_ext.lib.conf_parser import ConfParser


if __name__ == "__main__":

    # If '-' or '--help' provided parser exits 'automatically'
    # If wrong arguments are provided parser also exits, but with an error
    args = ArgsParser.getArguments()
    conf = ConfParser.Parse()

    pprint( args )
    pprint( conf )

    # execute operation
    #op = Operation.getOperation(args.command)(args, conf)


