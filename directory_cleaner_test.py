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
        self.temp_dir = tempfile.mkdtemp()

        files_and_directories1 = ["junk1", "junk2", "junk_dir/junk4",
                                  "caches/cache1/blah2", "caches/cache2/blah"
                                  "tasks/task1/task123", "tasks/task2/task234",]
        self.create_folders_and_files(self.temp_dir, files_and_directories1)

    def tearDown(self):
        # Remove the temporary directory and its contents after the test
        shutil.rmtree(self.temp_dir)

    def test_directory_cleaner(self):
        # directory_path = "/tmp/test-directory"
        exception_list = ["generic-worker.cfg", "tasks", "caches"]
        dc = directory_cleaner.DirectoryCleaner(self.temp_dir, exception_list)
        result = dc.clean_directory()
        print(result)
        assert result['deleted'] == [ str(Path(self.temp_dir) / 'junk2'), 
                                     str(Path(self.temp_dir) / 'junk1'), 
                                     str(Path(self.temp_dir) / 'junk_dir/junk4')]
        assert result['skipped'] == [ str(Path(self.temp_dir) / 'tasks'), 
                                     str(Path(self.temp_dir) / 'caches')]

if __name__ == '__main__':
    unittest.main()
