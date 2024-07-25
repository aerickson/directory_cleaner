#!/usr/bin/env python3

import os
from collections import deque


class DirectoryCleaner:
    def __init__(
        self,
        directory_path,
        exception_list,
        debug_mode=False,
        dry_run=False,
        remove_empty_directories=False,
    ):
        self.directory_path = directory_path
        self.exception_list = exception_list
        self.debug_mode = debug_mode
        self.dry_run = dry_run
        self.remove_empty_directories = remove_empty_directories
        self.result = {
            "skipped": [],
            "deleted_files": [],
            "deleted_directories": [],
            "errors": [],
            "deleted": [],  # Added to store all deleted items
        }

        if self.dry_run and self.debug_mode:
            print("INFO: Dry run mode enabled. No files will be deleted.")

    def _debug_print(self, message):
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

        self._debug_print(f"Cleaning directory '{self.directory_path}'...")
        self._clean_non_recursive()

        if self.remove_empty_directories:
            self._remove_empty_directories()

        # Combine deleted files and directories into the deleted field
        self.result["deleted"] = sorted(
            self.result["deleted_files"] + self.result["deleted_directories"]
        )

        # Print summary message
        print(
            f"Cleaned directory '{self.directory_path}'. Removed {len(self.result['deleted_files'])} files and {len(self.result['deleted_directories'])} directories."
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
                            self._debug_print(f"Removed file: {item_path}")
                            self.result["deleted_files"].append(item_path)
                        except Exception as e:
                            self._debug_print(f"Error removing file {item_path}: {e}")
                            self.result["errors"].append(item_path)
                else:
                    self._debug_print(f"Skipped file/directory: {item_path}")
                    self.result["skipped"].append(item_path)

        self.result["skipped"].sort()
        self.result["deleted_files"].sort()
        self.result["errors"].sort()

    def _remove_empty_directories(self):
        for root, dirs, files in os.walk(self.directory_path, topdown=False):
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                # Check if directory is empty and not in the exception list
                if not os.listdir(dir_path) and directory not in self.exception_list:
                    try:
                        if not self.dry_run:
                            os.rmdir(dir_path)
                        self._debug_print(f"Removed empty directory: {dir_path}")
                        self.result["deleted_directories"].append(dir_path)
                    except Exception as e:
                        self._debug_print(f"Error removing directory {dir_path}: {e}")
                        self.result["errors"].append(dir_path)

        self.result["deleted_directories"].sort()
        self.result["errors"].sort()
