"""
The command line interface
"""

import sys
import argparse
import dploy.main as main
import dploy.version as version


def create_parser():
    """
    create the CLI argument parser
    """
    parser = argparse.ArgumentParser(prog='dploy')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {version}'.format(version=version.__version__))
    parser.add_argument('--quiet',
                        dest='is_quiet',
                        action='store_true',
                        help='suppress normal output excluding error messages')
    parser.add_argument('--dry-run',
                        dest='is_dry_run',
                        action='store_true',
                        help='show what would be done without doing it')


    sub_parsers = parser.add_subparsers(dest="subcmd")

    stow_parser = sub_parsers.add_parser('stow')
    stow_parser.add_argument('source',
                             nargs='+',
                             help='source directory to stow')
    stow_parser.add_argument('dest',
                             help='destination path to stow into')

    stow_parser = sub_parsers.add_parser('unstow')
    stow_parser.add_argument('source',
                             nargs='+',
                             help='source directory to unstow from')
    stow_parser.add_argument('dest',
                             help='destination path to unstow')

    link_parser = sub_parsers.add_parser('link')
    link_parser.add_argument('source',
                             help='source file or directory to link')
    link_parser.add_argument('dest',
                             help='destination path to link')
    return parser


def run(arguments=None):
    """
    interpret the parser arguments and execute the corresponding commands
    """

    subcmd_map = {
        'stow': main.Stow,
        'unstow': main.UnStow,
        'link': main.Link,
    }

    try:
        parser = create_parser()

        if arguments is None:
            args = parser.parse_args()
        else:
            args = parser.parse_args(arguments)

        try:
            subcmd = subcmd_map[args.subcmd]
            subcmd(args.source,
                   args.dest,
                   is_silent=args.is_quiet,
                   is_dry_run=args.is_dry_run)
        except (ValueError, PermissionError) as error:
            print(error, file=sys.stderr)
            sys.exit(1)
        except KeyError:
            parser.print_help()

    except (KeyboardInterrupt) as error:
        print(error, file=sys.stderr)
        sys.exit(130)