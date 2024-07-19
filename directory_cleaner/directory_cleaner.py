#!/usr/bin/env python3

import os
from collections import deque
import argparse


class DirectoryCleaner:
    def __init__(self, directory_path, exception_list, debug_mode=False, dry_run=False):
        self.directory_path = directory_path
        self.exception_list = exception_list
        self.debug_mode = debug_mode
        self.dry_run = dry_run
        self.result = {"skipped": [], "deleted": [], "errors": []}

        if self.dry_run and self.debug_mode:
            print("INFO: Dry run mode enabled. No files will be deleted.")

    def debug_print(self, message):
        if self.debug_mode:
            if self.dry_run:
                print(f"DRY_RUN: {message}")
            else:
                print(message)

    def clean_directory(self):
        if not os.path.exists(self.directory_path):
            print(f"Directory '{self.directory_path}' does not exist.")
            self.result["errors"].append(self.directory_path)
            return self.result

        self.debug_print(f"Cleaning directory '{self.directory_path}'...")
        self._clean_non_recursive()
        self._remove_empty_directories()
        print(
            f"Cleaned directory '{self.directory_path}'. Removed {len(self.result['deleted'])} files and directories."
        )
        return self.result

    def _clean_non_recursive(self):
        stack = deque([self.directory_path])

        while stack:
            current_path = stack.pop()

            for item in os.listdir(current_path):
                item_path = os.path.join(current_path, item)

                # Check if the file/directory is in the exception list
                if item not in self.exception_list:
                    if os.path.isdir(item_path):
                        stack.append(item_path)
                    elif os.path.isfile(item_path):
                        # If not in the exception list, remove the file
                        try:
                            if not self.dry_run:
                                os.remove(item_path)
                            self.debug_print(f"Removed file: {item_path}")
                            self.result["deleted"].append(item_path)
                        except Exception as e:
                            self.debug_print(f"Error removing file {item_path}: {e}")
                            self.result["errors"].append(item_path)
                else:
                    self.debug_print(f"Skipped file/directory: {item_path}")
                    self.result["skipped"].append(item_path)

        self.result["skipped"].sort()
        self.result["deleted"].sort()
        self.result["errors"].sort()

    def _remove_empty_directories(self):
        for root, dirs, files in os.walk(self.directory_path, topdown=False):
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                if not os.listdir(dir_path):  # Check if directory is empty
                    try:
                        if not self.dry_run:
                            os.rmdir(dir_path)
                        self.debug_print(f"Removed empty directory: {dir_path}")
                        self.result["deleted"].append(dir_path)
                    except Exception as e:
                        self.debug_print(f"Error removing directory {dir_path}: {e}")
                        self.result["errors"].append(dir_path)

        self.result["deleted"].sort()
        self.result["errors"].sort()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Clean a directory by removing specified files and directories."
    )
    parser.add_argument("directory_path", help="Path of the directory to clean")
    parser.add_argument(
        "exception_list", nargs="+", help="List of files and directories to skip"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Enable dry run mode (no files will be deleted)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    cleaner = DirectoryCleaner(
        directory_path=args.directory_path,
        exception_list=args.exception_list,
        debug_mode=args.debug,
        dry_run=args.dry_run,
    )

    result = cleaner.clean_directory()

    import pprint

    pprint.pprint(result)
