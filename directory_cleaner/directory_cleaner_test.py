import unittest
import tempfile
import pytest
import os
import shutil
import subprocess
from pathlib import Path

import directory_cleaner.directory_cleaner as DC

test_cases = [
    pytest.param(["directory_cleaner"], None, 2, id="no args"),
    pytest.param(["directory_cleaner", "--help"], None, 0, id="help"),
    pytest.param(["directory_cleaner", "--version"], None, 0, id="version"),
    pytest.param(
        ["directory_cleaner", "-c", "configs/taskcluster_unix.toml", "PATH"],
        None,
        0,
        id="basic config",
    ),
    pytest.param(
        [
            "directory_cleaner",
            "-c",
            "configs/taskcluster_unix.toml",
            "PATH",
            "-d",
            "-v",
        ],
        None,
        0,
        id="basic config (dry run and verbose)",
    ),
    pytest.param(
        ["directory_cleaner", "-c", "configs/bad.toml", "PATH"],
        None,
        1,
        id="non-existent config",
    ),
    pytest.param(
        ["directory_cleaner", "-c", "configs/testing_only/bad.toml", "PATH"],
        None,
        1,
        id="malformed config",
    ),
    pytest.param(
        ["directory_cleaner", "-c", "configs/testing_only/missing.toml", "PATH"],
        None,
        1,
        id="missing required entry in config",
    ),
]


class TestApp:
    @pytest.mark.parametrize(
        "command, expected_output, expected_result_code", test_cases
    )
    def test_app(self, command, expected_output, expected_result_code, tmp_path):
        for item in command:
            if item == "PATH":
                command[command.index(item)] = str(tmp_path)
        env = os.environ.copy()
        result = subprocess.run(command, capture_output=True, text=True, env=env)
        output = result.stdout.rstrip()
        assert result.returncode == expected_result_code
        if expected_output:
            assert output == expected_output


class TestFileOperations:
    def create_folders_and_files(self, root_dir, paths):
        for path in paths:
            full_path = os.path.join(root_dir, path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            Path(full_path).touch()

    def setup_method(self, _method):
        # test dir 1
        self.temp_dir1 = tempfile.mkdtemp()

        files_and_directories1 = [
            "junk1",
            "junk2",
            "junk_dir/junk4",
            "caches/cache1/blah2",
            "caches/cache2/blah" "tasks/task1/task123",
            "tasks/task2/task234",
            "misc2/",
            "misc/blah.txt",
            "generic-worker.cfg",
            "generic-worker.cfg.bak",
        ]
        self.create_folders_and_files(self.temp_dir1, files_and_directories1)

    def teardown_method(self, _method):
        # Remove the temporary directory and its contents after the test
        shutil.rmtree(self.temp_dir1)

    def test_directory_cleaner(self):
        exception_list = ["generic-worker.cfg", "tasks", "caches", "misc2"]
        dc = DC.DirectoryCleaner(self.temp_dir1, exception_list)
        result = dc.clean_directory()
        # print(result)
        assert result["deleted"] == sorted(
            [
                str(Path(self.temp_dir1) / "generic-worker.cfg.bak"),
                str(Path(self.temp_dir1) / "junk1"),
                str(Path(self.temp_dir1) / "junk2"),
                str(Path(self.temp_dir1) / "junk_dir"),
                str(Path(self.temp_dir1) / "junk_dir/junk4"),
                str(Path(self.temp_dir1) / "misc"),
                str(Path(self.temp_dir1) / "misc/blah.txt"),
            ]
        )
        assert result["skipped"] == sorted(
            [
                str(Path(self.temp_dir1) / "tasks"),
                str(Path(self.temp_dir1) / "generic-worker.cfg"),
                str(Path(self.temp_dir1) / "misc2"),
                str(Path(self.temp_dir1) / "caches"),
            ]
        )

    def test_directory_cleaner_non_existent(self):
        exception_list = ["generic-worker.cfg", "tasks", "caches"]
        dc = DC.DirectoryCleaner("/tmp/z838a8ca8a88c", exception_list)
        result = dc.clean_directory()
        assert result["errors"] == ["/tmp/z838a8ca8a88c"]

    def test_directory_cleaner_verbose(self):
        exception_list = ["generic-worker.cfg", "tasks", "caches"]
        # sets debug_mode=True to test printing of debug messages
        dc = DC.DirectoryCleaner(self.temp_dir1, exception_list, debug_mode=True)
        _result = dc.clean_directory()

    def test_directory_cleaner_exception(self, mocker):
        exception_list = ["generic-worker.cfg", "tasks", "caches"]
        dc = DC.DirectoryCleaner(self.temp_dir1, exception_list)
        mocker.patch("os.remove", side_effect=FileNotFoundError("File not found"))
        _result = dc.clean_directory()
        os.remove.assert_called()


if __name__ == "__main__":
    unittest.main()
