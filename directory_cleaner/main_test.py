import pytest
import unittest
import os
import subprocess


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


if __name__ == "__main__":
    unittest.main()
