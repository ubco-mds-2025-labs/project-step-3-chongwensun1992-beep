import unittest
from unittest.mock import patch
from smartbudget.core_module_2.file_io_data_controller import FileIoDataStorageController


class TestFileIoDataController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n[FileIoController] setUpClass")

    def setUp(self):
        self.controller = FileIoDataStorageController()

    @patch("smartbudget.core_module_2.file_io_data_controller.clear_json")
    def test_clear_data(self, mock_clear):
        with patch("builtins.input", return_value="y"):
            self.controller.clear_data()
        mock_clear.assert_called_once()

    @patch("smartbudget.core_module_2.file_io_data_controller.save_to_json")
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json")
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=False)
    def test_save_data(self, mock_exists, mock_load, mock_save):
        mock_load.return_value = [{"name": "A"}]

        with patch("builtins.input", return_value="backup1.json"):
            self.controller.save_data()

        mock_load.assert_called_once()
        mock_save.assert_called_once()

    def tearDown(self):
        self.controller = None

    @classmethod
    def tearDownClass(cls):
        print("[FileIoController] tearDownClass\n")



