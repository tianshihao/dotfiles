import argparse
import sys

from .manager import Manager


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Manage configuration synchronization.')
    parser.add_argument('--retrieve', action='store_true',
                        help='Retrieve configurations from the host')
    parser.add_argument('--dispatch', action='store_true',
                        help='Dispatch configurations to the host')
    parser.add_argument('--validate', action='store_true',
                        help='Output the configurations that will be synchronized (dry run)')

    args = parser.parse_args()

    manager = Manager()

    if args.dispatch:
        manager.dispatch_to_host()
    elif args.retrieve:
        manager.retrieve_from_host()
    elif args.validate:
        manager.validate()
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    main()
