#!/usr/bin/env python3

import os
from collections import deque


class DirectoryCleaner:
    def __init__(self, directory_path, exception_list, debug_mode=False, dry_run=False):
        self.directory_path = directory_path
        self.exception_list = exception_list
        self.debug_mode = debug_mode
        self.dry_run = dry_run

    def debug_print(self, a_string):
        if self.debug_mode:
            print(a_string)

    def clean_directory(self):
        if not os.path.exists(self.directory_path):
            print(f"Directory '{self.directory_path}' does not exist.")
            return {"errors": [self.directory_path]}

        self.debug_print(f"Cleaning directory: {self.directory_path}")
        result = self._clean_non_recursive()
        return result

    def _clean_non_recursive(self):
        deleted_items = []
        skipped_items = []
        error_items = []
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
                            deleted_items.append(item_path)
                        except Exception as e:
                            self.debug_print(f"- Error removing file {item_path}: {e}")
                            error_items.append(item_path)
                else:
                    self.debug_print(f"- Skipped file/directory: {item_path}")
                    skipped_items.append(item_path)
        return {
            "skipped": skipped_items,
            "deleted": deleted_items,
            "errors": error_items,
        }


# if __name__ == "__main__":

# directory_path = "/tmp/test-directory"
# exception_list = ["generic-worker.cfg", "tasks", "cache"]
# "Downloads", "file_to_keep.txt", "important_document.docx"]

# cleaner = DirectoryCleaner(directory_path, exception_list)
# result = cleaner.clean_directory()

# import pprint
# pprint.pprint(result)
