import argparse
import sys
import os
import toml
import textwrap
import directory_cleaner.directory_cleaner as DC


def parse_config_file(config_path):
    try:
        with open(config_path, "r") as file:
            config = toml.load(file)
        if "exclusion_patterns" not in config:
            print(
                f"ERROR: Config file '{config_path}' is missing 'exclusion_patterns' key."
            )
            sys.exit(1)
        return config
    except FileNotFoundError:
        print(f"ERROR: Config file '{config_path}' not found!")
        sys.exit(1)
    except toml.TomlDecodeError as e:
        print(f"ERROR: Error parsing config file '{config_path}': {e}")
        sys.exit(1)


def get_version_from_pyproject():
    pyproject_toml = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pyproject.toml")
    )
    try:
        with open(pyproject_toml, "r") as toml_file:
            pyproject_data = toml.load(toml_file)
            return pyproject_data["tool"]["poetry"]["version"]
    except FileNotFoundError:
        return "Unknown"
    except toml.TomlDecodeError as e:
        print(f"ERROR: Error parsing pyproject.toml file: {e}")
        return "Unknown"


def main():
    parser = argparse.ArgumentParser(
        description="Remove all files and directories not in an exception list (in a specific directory).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
             Config file format (TOML):

             exclusion_patterns = [
                "directory_a",  # This directory and all files inside will be excluded from deletion
                "file_xyz"
             ]
             """
        ),
    )

    parser.add_argument(
        "--config",
        "-c",
        dest="config_file",
        type=str,
        required=True,
        help="Path to the config file in TOML format.",
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
    parser.add_argument(
        "--remove-empty-directories",
        "-r",
        dest="remove_empty_directories",
        action="store_true",
        help="Remove empty directories.",
    )
    parser.add_argument(
        "--version", action="version", version=get_version_from_pyproject()
    )
    parser.add_argument("directory", type=str, help="The directory to clean.")

    args = parser.parse_args()

    # Parse the config file
    config = parse_config_file(args.config_file)

    # Create a DirectoryCleaner object
    cleaner = DC.DirectoryCleaner(
        args.directory,
        config["exclusion_patterns"],
        dry_run=args.dry_run,
        debug_mode=args.verbose,
        remove_empty_directories=args.remove_empty_directories,
    )

    # Clean the directory
    cleaner.clean_directory()


if __name__ == "__main__":
    main()
