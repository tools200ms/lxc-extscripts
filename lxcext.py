from pprint import pprint

from lxc_ext import Operation
from lxc_ext.lib.args_parser import ArgsParser
from lxc_ext.lib.conf_parser import ConfParser

# Format:
# <client|server>.<generic>.<specific>[-detailed]

if __name__ == "__main__":

    # If '-' or '--help' provided parser exits 'automatically'
    # If wrong arguments are provided parser also exits, but with an error
    args = ArgsParser()
    conf = ConfParser.Parse(args.getConfigFilePath())

    options = args.merge(conf)

    op = Operation.getOperation(options)

    op.start()
    #pprint(conf)
    #pprint(options)

    # execute operation
    #op = Operation.getOperation(args.command)(args, conf)


