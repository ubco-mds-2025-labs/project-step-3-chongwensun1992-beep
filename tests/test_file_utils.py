import os
import shutil
import unittest
from unittest.mock import patch


import smartbudget.file_io_module_3.file_utils as fu


class TestFileUtils(unittest.TestCase):

    TEST_DIR = "files"

    def setUp(self):

        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)
        os.makedirs(self.TEST_DIR, exist_ok=True)

    def tearDown(self):

        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)

    # ------------------------------
    # ensure_files_dir()
    # ------------------------------
    def test_ensure_files_dir_creates_directory(self):
        shutil.rmtree(self.TEST_DIR)  # 删除后看能否重新创建
        fu.ensure_files_dir()
        self.assertTrue(os.path.exists(self.TEST_DIR))

    # ------------------------------
    # file_exists()
    # ------------------------------
    def test_file_exists_true(self):
        target = os.path.join(self.TEST_DIR, "test.txt")
        with open(target, "w") as f:
            f.write("hello")

        self.assertTrue(fu.file_exists("test.txt"))

    def test_file_exists_false(self):
        self.assertFalse(fu.file_exists("no_file.json"))

    # ------------------------------
    # delete_file()
    # ------------------------------
    def test_delete_file_success(self):
        target = os.path.join(self.TEST_DIR, "del.txt")
        with open(target, "w") as f:
            f.write("bye")

        self.assertTrue(fu.delete_file("del.txt"))
        self.assertFalse(os.path.exists(target))

    def test_delete_file_not_found(self):
        self.assertFalse(fu.delete_file("ghost.txt"))

    # ------------------------------
    # list_files()
    # ------------------------------
    def test_list_files(self):
        files = ["a.txt", "b.json", "c.data"]
        for f in files:
            with open(os.path.join(self.TEST_DIR, f), "w") as fp:
                fp.write("x")

        listed = fu.list_files()
        self.assertCountEqual(listed, files)

    def test_list_files_empty(self):
        """目录空时返回空列表"""
        self.assertEqual(fu.list_files(), [])

    # ------------------------------
    # ensure_files_dir with mocked os.path.exists
    #
    # ------------------------------
    @patch("os.path.exists", return_value=False)
    @patch("os.makedirs")
    def test_ensure_files_dir_calls_makedirs(self, mock_makedirs, mock_exists):
        fu.ensure_files_dir()
        mock_makedirs.assert_called_once()


