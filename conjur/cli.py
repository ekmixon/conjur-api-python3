# -*- coding: utf-8 -*-

"""
CLI module

This module is the main entrypoint for all CLI-like usages of this
module where only the minimal invocation configuration is required.
"""

import argparse
import json
import os
import sys

from .client import Client

from .version import __version__

class MyParser(argparse.ArgumentParser):
   def error(self, message):
        sys.stderr.write('Error %s\n' % message)
        self.print_help()
        exit(1)

   def liav_error(self, message, help):
        sys.stderr.write('Error %s\n' % message)
        sys.stderr.write('%s\n' % help)
        exit(1)

   def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        action = args.resource if args else None
        print(action)
        if argv:
            print(argv)
            msg = 'unrecognized arguments: %s'
            err_msg = (msg % ' '.join(argv))
            if action:
                # find the subparser for requesting action (list/whoami)
                c_help = self._subparsers._actions[0].choices.get(action)
                if c_help:
                    # format_help prints the help for each respective action
                    self.liav_error(err_msg, c_help.format_help())
                else:
                    self.error(err_msg)
            else:
                self.error(err_msg)
        return args

class Cli():
    """
    Main wrapper around CLI-like usages of this module. Provides various
    helpers around parsing of parameters and running client commands.
    """
    #pylint: disable=no-self-use

    def des(name=None):
        return '''
*****************************************************************
*   Conjur’s CLI for managing roles, resources and privileges   *
*****************************************************************
Copyright © 1999-2020 CyberArk Software Ltd. All rights reserved.

Usage:
    conjur [global options] command subcommand [options] [arguments…]'''

# def variable_description(name=None):
#         return '''
# Usage:
#     conjur [global options] command subcommand [arguments…]'''

    def run(self, *args):
        """
        Main entrypoint for the class invocation from both CLI, Package, and
        test sources. Parses CLI args and invokes the appropriate client command.
        """
        parser = MyParser(description=self.des(),
                          epilog="CONJUR",
                          usage=argparse.SUPPRESS, add_help=False, formatter_class=argparse.RawTextHelpFormatter)
        # parser = argparse.ArgumentParser(description='Conjur Pythonss3 API CLI')

        globals_optionals = parser.add_argument_group("Global arguments")
        resource_subparsers = parser.add_subparsers(dest='resource', title="Commands")

        resource_subparsers.add_parser('whoami',
            help='Provides information about the user making an API request.')

        list_subparsers = resource_subparsers.add_parser('list')
        list_subparsers.add_argument('-k', '--kind')

        #list_subparsers.add_argument('-l', '--url')

        variable_parser = resource_subparsers.add_parser('variable', description="sgal",
            help='Perform variable-related actions . See "variable -help" for more options', add_help=False, usage='conjur [global options] command subcommand [options] [arguments…]')

        variable_subparsers = variable_parser.add_subparsers(dest='action', title="Subcommands")
        get_variable_parser = variable_subparsers.add_parser('get',
            help='Get the value of a variable')
        set_variable_parser = variable_subparsers.add_parser('set',
            help='Set the value of a variable')

        glob_option = variable_parser.add_argument_group("Global arguments")
        glob_option.add_argument('-h', '--help', action='help', help="show this help message and exit")

        get_variable_parser.add_argument('variable_id',
            help='ID of a variable', nargs='+')

        set_variable_parser.add_argument('variable_id',
            help='ID of the variable')
        set_variable_parser.add_argument('value',
            help='New value of the variable')

        policy_parser = resource_subparsers.add_parser('policy',
            help='Perform policy-related actions . See "policy -help" for more options')
        policy_subparsers = policy_parser.add_subparsers(dest='action')

        apply_policy_parser = policy_subparsers.add_parser('apply',
            help='Apply a policy file')
        apply_policy_parser.add_argument('name',
            help='Name of the policy (usually "root")')
        apply_policy_parser.add_argument('policy',
            help='File containing the YAML policy')

        replace_policy_parser = policy_subparsers.add_parser('replace',
            help='Replace a policy file')
        replace_policy_parser.add_argument('name',
            help='Name of the policy (usually "root")')
        replace_policy_parser.add_argument('policy',
            help='File containing the YAML policy')

        delete_policy_parser = policy_subparsers.add_parser('delete',
            help='Delete a policy file')
        delete_policy_parser.add_argument('name',
            help='Name of the policy (usually "root")')
        delete_policy_parser.add_argument('policy',
            help='File containing the YAML policy')


        globals_optionals.add_argument('-h', '--help', action='help', help="show this help message and exit")
        globals_optionals.add_argument('-v', '--version', action='version',
            version='%(prog)s v' + __version__)

        globals_optionals.add_argument('-l', '--url')
        globals_optionals.add_argument('-a', '--account')

        globals_optionals.add_argument('-c', '--ca-bundle')
        globals_optionals.add_argument('--insecure',
            help='Skip verification of server certificate (not recommended)',
            dest='ssl_verify',
            action='store_false')

        # The external names for these are unfortunately named so we remap them
        globals_optionals.add_argument('-u', '--user', dest='login_id')
        globals_optionals.add_argument('-k', '--api-key')
        globals_optionals.add_argument('-p', '--password')

        globals_optionals.add_argument('-d', '--debug',
            help='Enable debugging output',
            action='store_true')

        globals_optionals.add_argument('--verbose',
            help='Enable verbose debugging output',
            action='store_true')


        resource, args = Cli._parse_args(parser)

        # We don't have a good "debug" vs "verbose" separation right now
        if args.verbose is True:
            args.debug = True
        try:
            Cli.run_client_action(resource, args)
        except Exception as e:
            print(e)
        else:
            # Explicit exit (required for tests)
            sys.exit(0)

    @staticmethod
    def run_client_action(resource, args):
        print("Resource " + resource)
        print(args)
        """
        Helper for creating the Client instance and invoking the appropriate
        api class method with the specified parameters.
        """

        ca_bundle = None
        if args.ca_bundle:
            ca_bundle = os.path.expanduser(args.ca_bundle)

        # We want explicit definition of things to pass into the client
        # to avoid ambiguity
        client = Client(url=args.url,
                        account=args.account,
                        api_key=args.api_key,
                        login_id=args.login_id,
                        password=args.password,
                        ssl_verify=args.ssl_verify,
                        ca_bundle=ca_bundle,
                        debug=args.debug)

        if resource == 'list':
            result = client.list()
            print(json.dumps(result, indent=4))
        elif resource == 'whoami':
            result = client.whoami()
            print(json.dumps(result, indent=4))
        elif resource == 'variable':
            variable_id = args.variable_id
            if args.action == 'get':
                if len(variable_id) == 1:
                    variable_value = client.get(variable_id[0])
                    print(variable_value.decode('utf-8'), end='')
                else:
                    variable_values = client.get_many(*variable_id)
                    print(json.dumps(variable_values, indent=4))
            else:
                client.set(variable_id, args.value)
                print("Value set: '{}'".format(variable_id))
        elif resource == 'policy':
            if args.action == 'replace':
                resources = client.replace_policy_file(args.name, args.policy)
                print(json.dumps(resources, indent=4))
            elif args.action == 'delete':
                resources = client.delete_policy_file(args.name, args.policy)
                print(json.dumps(resources, indent=4))
            else:
                resources = client.apply_policy_file(args.name, args.policy)
                print(json.dumps(resources, indent=4))


    @staticmethod
    def _parse_args(parser):
        args = parser.parse_args()

        if not args.resource:
            parser.print_help()
            sys.exit(0)

        # Check whether we are running a command with required additional
        # arguments and if so, validate that those additional arguments are present
        if args.resource not in ['list', 'whoami']:
            if 'action' not in args or not args.action:
                parser.print_help()
                sys.exit(0)

        return args.resource, args

    @staticmethod
    def launch():
        """
        Static wrapper around instantiating and invoking the CLI that
        """
        Cli().run()

if __name__ == '__main__':
    # Not coverage-tested since the integration tests do this
    Cli.launch() # pragma: no cover
