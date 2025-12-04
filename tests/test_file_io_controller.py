import unittest
from unittest.mock import patch, MagicMock
from smartbudget.core_module_2.file_io_data_controller import FileIoDataStorageController
from smartbudget.entity.income import Income
from smartbudget.entity.expense import Expense


class TestFileIoDataController(unittest.TestCase):

    def setUp(self):
        self.ctrl = FileIoDataStorageController()

        # mute all print()
        self.patcher = patch("builtins.print")
        self.mock_print = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    # ---------------- clear_data ----------------
    @patch("builtins.input", return_value="y")
    @patch("smartbudget.core_module_2.file_io_data_controller.clear_json")
    def test_clear_data_yes(self, mock_clear, _):
        self.ctrl.clear_data()
        mock_clear.assert_called_once()

    @patch("builtins.input", return_value="n")
    @patch("smartbudget.core_module_2.file_io_data_controller.clear_json")
    def test_clear_data_no(self, mock_clear, _):
        self.ctrl.clear_data()
        mock_clear.assert_not_called()

    # ---------------- save_data ----------------
    @patch("builtins.input", side_effect=["backup.json", "y"])
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=True)
    @patch("smartbudget.core_module_2.file_io_data_controller.save_to_json")
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json", return_value=[{"x": 1}])
    def test_save_data_overwrite(self, *_):
        self.ctrl.save_data()

    @patch("builtins.input", return_value="")
    def test_save_data_empty(self, _):
        self.ctrl.save_data()

    @patch("builtins.input", return_value="records.json")
    def test_save_data_block_system_file(self, _):
        self.ctrl.save_data()

    # ---------------- load_data ----------------
    @patch("builtins.input", return_value="file.json")
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=False)
    def test_load_data_not_exist(self, *_):
        incomes, expenses = [], []
        self.ctrl.load_data(incomes, expenses)
        self.assertEqual(incomes, [])
        self.assertEqual(expenses, [])

    @patch("builtins.input", return_value="file.json")
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=True)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json")
    def test_load_data_success(self, mock_load, *_):
        mock_load.return_value = [
            Income("Salary", 100, "Work"),
            Expense("Food", 10, "Groceries")
        ]
        incomes, expenses = [], []
        self.ctrl.load_data(incomes, expenses)
        self.assertEqual(len(incomes), 1)
        self.assertEqual(len(expenses), 1)

    # ---------------- show_files ----------------
    @patch("smartbudget.core_module_2.file_io_data_controller.list_files", return_value=["a.json", "records.json"])
    def test_show_files(self, _):
        self.ctrl.show_files()

    # ---------------- delete_backup_file ----------------
    @patch("builtins.input", return_value="")
    def test_delete_empty(self, _):
        self.ctrl.delete_backup_file()

    @patch("builtins.input", return_value="records.json")
    def test_delete_system_file(self, _):
        self.ctrl.delete_backup_file()

    @patch("builtins.input", return_value="old.json")
    @patch("smartbudget.core_module_2.file_io_data_controller.delete_file", return_value=True)
    def test_delete_success(self, *_):
        self.ctrl.delete_backup_file()

    @patch("builtins.input", return_value="old.json")
    @patch("smartbudget.core_module_2.file_io_data_controller.delete_file", return_value=False)
    def test_delete_not_found(self, *_):
        self.ctrl.delete_backup_file()
