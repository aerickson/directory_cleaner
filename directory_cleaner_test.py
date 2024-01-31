import unittest
import tempfile
import os

class TestFileOperations(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.temp_dir = tempfile.mkdtemp()

        # Create some test files in the temporary directory
        self.file1_path = os.path.join(self.temp_dir, 'file1.txt')
        with open(self.file1_path, 'w') as file1:
            file1.write('Hello, this is file1 content.')

        self.file2_path = os.path.join(self.temp_dir, 'file2.txt')
        with open(self.file2_path, 'w') as file2:
            file2.write('Hello, this is file2 content.')

    def tearDown(self):
        # Remove the temporary directory and its contents after the test
        os.rmdir(self.temp_dir)

    def test_file_existence(self):
        # Test if the files were created successfully
        self.assertTrue(os.path.isfile(self.file1_path))
        self.assertTrue(os.path.isfile(self.file2_path))

    def test_file_content(self):
        # Test if the content of the files is as expected
        with open(self.file1_path, 'r') as file1:
            content1 = file1.read()
        self.assertEqual(content1, 'Hello, this is file1 content.')

        with open(self.file2_path, 'r') as file2:
            content2 = file2.read()
        self.assertEqual(content2, 'Hello, this is file2 content.')

    # Add more test methods as needed

if __name__ == '__main__':
    unittest.main()
