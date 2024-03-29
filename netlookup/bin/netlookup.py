#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI 'netlookup' main entry point
"""
from cli_toolkit.script import Script

from .commands.info import Info
from .commands.prefixes import PrefixLookup
from .commands.split import Split
from .commands.substract import Subtract


class NetLookupScript(Script):
    """
    Netlookup CLI command
    """
    subcommands = (
        Info,
        PrefixLookup,
        Split,
        Subtract,
    )


def main():
    """
    Main function for 'netlookup' CLI command
    """
    NetLookupScript().run()
