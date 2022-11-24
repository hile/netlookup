
from cli_toolkit.script import Script

from .commands.info import Info
from .commands.prefixes import PrefixLookup
from .commands.split import Split
from .commands.substract import Subtract


class NetLookupScript(Script):
    """
    Netlookup CLI command
    """


def main():
    """
    Main function for 'netlookup' CLI command
    """
    script = NetLookupScript()

    script.add_subcommand(Info(script))
    script.add_subcommand(PrefixLookup(script))
    script.add_subcommand(Split(script))
    script.add_subcommand(Subtract(script))

    script.run()
