#!/usr/bin/env python2

""" Python implementation fo T05 language entry point. """

import t05_State
import t05_CommandLineInterface
import sys


def main(args):
    state = t05_State.State()
    state.init()
    cli = t05_CommandLineInterface.CommandLineInterface()
    cli.init(state, args)
    if len(args) < 2:
        #cli.addInputFile("x.t05")
        cli.addInputFile("testsuite/test013.t05")
    cli.run()
    return 0


if __name__ == '__main__':
    main(sys.argv)
