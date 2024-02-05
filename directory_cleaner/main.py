import argparse
import sys
import toml
import textwrap

import directory_cleaner.directory_cleaner as DC


def parse_config_file(config_path):
    with open(config_path, "r") as file:
        config = toml.load(file)
    return config


def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(
        description="Delete items in a directory while excluding certain items.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
         config file format (toml):

            exclusion_patterns = [
                            'directory_a',  # all files in this directory be excluded from deletion
                            'file_xyz',
                        ]

         """
        ),
    )

    # Add command line argument for config file path
    parser.add_argument(
        "--config",
        "-c",
        dest="config_file",
        type=str,
        required=True,
        help="Path to the config file in INI format.",
    )
    parser.add_argument(
        "--dry-run",
        "-d",
        dest="dry_run",
        action="store_true",
        help="Don't delete anything, just print what would be deleted.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        dest="verbose",
        action="store_true",
        help="Print debug information.",
    )
    # TODO: make dry run the default and add a --force option
    parser.add_argument("directory", type=str, help="The directory to clean.")

    # Parse command line arguments
    args = parser.parse_args()
    # print(args)

    # TODO: verify the config file exists

    # Parse the config file
    config_path = args.config_file
    try:
        config = parse_config_file(config_path)
    except FileNotFoundError:
        print(f"ERROR: Config file '{config_path}' not found!")
        sys.exit(1)

    # debugging: print the parsed config
    # for key, value in config.items():
    #     print(f'{key} = {value}')

    # Create a DirectoryCleaner object
    cleaner = DC.DirectoryCleaner(
        args.directory,
        config["exclusion_patterns"],
        dry_run=args.dry_run,
        debug_mode=args.verbose,
    )
    cleaner.clean_directory()


if __name__ == "__main__":
    main()
