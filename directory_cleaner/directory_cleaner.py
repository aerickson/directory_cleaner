#!/usr/bin/env python3

import os
from collections import deque


class DirectoryCleaner:
    def __init__(self, directory_path, exception_list, debug_mode=False, dry_run=False):
        self.directory_path = directory_path
        self.exception_list = exception_list
        self.debug_mode = debug_mode
        self.dry_run = dry_run
        self.result = {"skipped": [], "deleted": [], "errors": []}

        if self.dry_run and self.debug_mode:
            print("INFO: Dry run mode enabled. No files will be deleted.")

    def debug_print(self, a_string):
        if self.debug_mode:
            if self.dry_run:
                print(f"DRY_RUN: {a_string}")
            else:
                print(a_string)

    def clean_directory(self):
        if not os.path.exists(self.directory_path):
            print(f"Directory '{self.directory_path}' does not exist.")
            self.result["errors"].append(self.directory_path)
            return self.result

        self.debug_print(f"Cleaning directory: {self.directory_path}")
        self._clean_non_recursive()
        self._remove_empty_directories()
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
                            self.debug_print(f"- Removed file: {item_path}")
                            self.result["deleted"].append(item_path)
                        except Exception as e:
                            self.debug_print(f"- Error removing file {item_path}: {e}")
                            self.result["errors"].append(item_path)
                else:
                    self.debug_print(f"- Skipped file/directory: {item_path}")
                    self.result["skipped"].append(item_path)

        self.result["skipped"] = sorted(self.result["skipped"])
        self.result["deleted"] = sorted(self.result["deleted"])
        self.result["errors"] = sorted(self.result["errors"])

    def _remove_empty_directories(self):
        for root, dirs, files in os.walk(self.directory_path, topdown=False):
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                if not os.listdir(dir_path):  # Check if directory is empty
                    try:
                        if not self.dry_run:
                            os.rmdir(dir_path)
                        self.debug_print(f"- Removed empty directory: {dir_path}")
                        self.result["deleted"].append(dir_path)
                    except Exception as e:
                        self.debug_print(f"- Error removing directory {dir_path}: {e}")
                        self.result["errors"].append(dir_path)

        self.result["deleted"] = sorted(self.result["deleted"])
        self.result["errors"] = sorted(self.result["errors"])


# if __name__ == "__main__":
#     directory_path = "/tmp/test-directory"
#     exception_list = ["generic-worker.cfg", "tasks", "cache", "Downloads", "file_to_keep.txt", "important_document.docx"]
#     cleaner = DirectoryCleaner(directory_path, exception_list, debug_mode=True, dry_run=True)
#     result = cleaner.clean_directory()
#     import pprint
#     pprint.pprint(result)
