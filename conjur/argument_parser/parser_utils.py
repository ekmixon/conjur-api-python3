"""
This Module holds all the utils needed for the ArgParseBuilder
"""

import argparse
import time


def formatter(prog):
    """
    This method format the text of the different parsers.
    """
    return argparse.RawTextHelpFormatter(prog,
                                         max_help_position=100,
                                         width=100)


def header(*args):
    """
    This method builds the header for the main screen.
    """
    return '''Usage:
  {}'''.format(*args)


def command_description(example, usage):
    """
    This method builds the header for the main screen.
    """

    return f"\n\n Name:\n  {example}\n\nUsage:\n  {usage}"


def main_epilog():
    """
    This method builds the footer for the main help screen.
    """
    msg = "To get help on a specific command, see `conjur <command> -h | --help`\n\n"
    msg += "To start using Conjur with your environment, you must first initialize " \
           "the configuration. See `conjur init -h` for more information."
    return msg


def command_epilog(example, command=None, subcommands=None):
    """
    This method builds the footer for each command help screen.
    """
    refer_to_help = "See more details in each subcommand's help:"
    if subcommands:
        res = ""
        res += " -h\n".join(f"conjur {command} {subcommand}" for subcommand in subcommands)
        return f"{refer_to_help}\n{res}"
    return f"Examples:\n    {example}"


def title_formatter(title):
    """
    This method builds a reusable title for each argument section
    """
    return f"\n{title}"


def conjur_copyright():
    """
    This method builds the copyright description
    """
    msg = f'\nCopyright (c) {time.strftime("%Y")} CyberArk Software Ltd. All rights reserved.\n'
    msg += "<www.cyberark.com>\n"
    return msg
