import argparse
import logging
import sys

from .logging_helper import setup_logger
from .manager import Manager
from .utils import get_absolute_path


def main() -> None:
    setup_logger()

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Manage configuration synchronization.')
    parser.add_argument('--validate', action='store_true',
                        help='Validate the settings loaded from the configuration file')
    parser.add_argument('--overview', action='store_true',
                        help='Output the configurations that will be synchronized (dry run)')
    parser.add_argument('--retrieve', action='store_true',
                        help='Retrieve configurations from the host')
    parser.add_argument('--dispatch', action='store_true',
                        help='Dispatch configurations to the host')
    parser.add_argument('--settings', type=str, default='settings.json',
                        help='Path to the settings file (default: settings.json)')
    parser.add_argument('--app', type=str, nargs='+', default=None,
                        help='Only operate on the specified application(s) (by name, space separated)')

    args = parser.parse_args()

    try:
        manager: Manager = Manager(
            settings_path=get_absolute_path(args.settings),
            app_filter=args.app)
    except Exception as e:
        logging.error(f"Failed to initialize Manager: {e}", exc_info=True)
        sys.exit(1)

    if args.validate:
        manager.validate()
    elif args.overview:
        manager.overview()
    elif args.retrieve:
        manager.retrieve_from_host()
    elif args.dispatch:
        manager.dispatch_to_host()
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    main()
