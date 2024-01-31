#!/usr/bin/env python3

import unittest
import tempfile
import os
import shutil
from pathlib import Path

import directory_cleaner

class TestFileOperations(unittest.TestCase):
    def create_folders_and_files(self, root_dir, paths):
        for path in paths:
            full_path = os.path.join(root_dir, path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            Path(full_path).touch()

    def setUp(self):
        # test dir 1

        # Create a temporary directory
        self.temp_dir = tempfile.mkdtemp()

        files_and_directories1 = ["junk1", "junk2", "junk_dir/junk4",
                                  "caches/cache1/blah2", "caches/cache2/blah"
                                  "tasks/task1/task123", "tasks/task2/task234",]
        self.create_folders_and_files(self.temp_dir, files_and_directories1)

    def tearDown(self):
        # Remove the temporary directory and its contents after the test
        shutil.rmtree(self.temp_dir)

    # def test_file_existence(self):
    #     # Test if the files were created successfully
    #     self.assertTrue(os.path.isfile(self.file1_path))
    #     self.assertTrue(os.path.isfile(self.file2_path))

    def test_directory_cleaner(self):
        # directory_path = "/tmp/test-directory"
        exception_list = ["generic-worker.cfg", "tasks", "caches"]
        dc = directory_cleaner.DirectoryCleaner(self.temp_dir, exception_list)
        result = dc.clean_directory()
        # TODO: do asserts on result

    # def test_file_content(self):
    #     # Test if the content of the files is as expected
    #     with open(self.file1_path, 'r') as file1:
    #         content1 = file1.read()
    #     self.assertEqual(content1, 'Hello, this is file1 content.')

    #     with open(self.file2_path, 'r') as file2:
    #         content2 = file2.read()
    #     self.assertEqual(content2, 'Hello, this is file2 content.')

    # Add more test methods as needed

if __name__ == '__main__':
    unittest.main()
