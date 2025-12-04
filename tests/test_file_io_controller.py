import unittest
from unittest.mock import patch, MagicMock
from smartbudget.core_module_2.file_io_data_controller import FileIoDataStorageController
from smartbudget.entity.base_record import SmartBudgetError


class TestFileIoDataController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n[FileIO] setUpClass")

    def setUp(self):
        self.ctrl = FileIoDataStorageController()

    # =========================================================
    # clear_data()
    # =========================================================
    @patch("builtins.input", return_value="y")
    @patch("smartbudget.core_module_2.file_io_data_controller.clear_json")
    def test_clear_data_yes(self, mock_clear, mock_input):
        self.ctrl.clear_data()
        mock_clear.assert_called_once()

    @patch("builtins.input", return_value="n")
    def test_clear_data_no(self, mock_input):
        self.ctrl.clear_data()  # should print “cancelled”

    @patch("builtins.input", return_value="y")
    @patch("smartbudget.core_module_2.file_io_data_controller.clear_json",
            side_effect=Exception("fail"))
    def test_clear_data_clear_error(self, *_):
        self.ctrl.clear_data()  # handled by inner except and DOES NOT crash

    # =========================================================
    # save_data()
    # =========================================================
    @patch("builtins.input", side_effect=["backup.json", "y"])
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=True)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json", return_value=[1])
    @patch("smartbudget.core_module_2.file_io_data_controller.save_to_json")
    def test_save_data_overwrite(self, mock_save, mock_load, mock_exists, mock_input):
        self.ctrl.save_data()
        mock_save.assert_called_once()

    @patch("builtins.input", return_value="")
    def test_save_data_empty_filename(self, *_):
        self.ctrl.save_data()  # prints save error

    @patch("builtins.input", return_value="records.json")
    def test_save_data_block_system(self, *_):
        self.ctrl.save_data()  # cannot save to system file

    @patch("builtins.input", side_effect=["backup.json"])
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=False)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json",
           side_effect=Exception("load fail"))
    def test_save_data_load_error(self, *_):
        self.ctrl.save_data()  # triggers SmartBudgetError then prints

    @patch("builtins.input", side_effect=["backup.json"])
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=False)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json", return_value=[1])
    @patch("smartbudget.core_module_2.file_io_data_controller.save_to_json",
           side_effect=Exception("save fail"))
    def test_save_data_save_error(self, *_):
        self.ctrl.save_data()

    # unexpected error branch
    @patch("builtins.input", side_effect=["backup.json"])
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists",
           side_effect=Exception("boom"))
    def test_save_data_unexpected(self, *_):
        self.ctrl.save_data()

    # =========================================================
    # load_data()
    # =========================================================
    @patch("builtins.input", return_value="")
    def test_load_data_empty_filename(self, *_):
        self.ctrl.load_data([], [])  # error printed

    @patch("builtins.input", return_value="backup.json")
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=False)
    def test_load_data_missing_file(self, *_):
        incomes, expenses = [], []
        self.ctrl.load_data(incomes, expenses)
        self.assertEqual(incomes, [])
        self.assertEqual(expenses, [])

    @patch("builtins.input", return_value="backup.json")
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=True)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json",
           side_effect=Exception("load error"))
    def test_load_data_load_error(self, *_):
        self.ctrl.load_data([], [])

    @patch("builtins.input", return_value="backup.json")
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=True)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json",
           return_value=[object()])
    def test_load_data_processing_error(self, *_):
        # Because record is not Income or Expense, accessing describe() will fail
        self.ctrl.load_data([], [])

    @patch("builtins.input", return_value="backup.json")
    @patch("smartbudget.core_module_2.file_io_data_controller.file_exists", return_value=True)
    @patch("smartbudget.core_module_2.file_io_data_controller.load_from_json")
    def test_load_data_success(self, mock_load, *_):
        from smartbudget.entity.income import Income
        from smartbudget.entity.expense import Expense
        mock_load.return_value = [
            Income("Salary", 100, "Work"),
            Expense("Food", 10, "Groceries"),
        ]

        incomes, expenses = [], []
        self.ctrl.load_data(incomes, expenses)
        self.assertEqual(len(incomes), 1)
        self.assertEqual(len(expenses), 1)

    # =========================================================
    # show_files()
    # =========================================================
    @patch("smartbudget.core_module_2.file_io_data_controller.list_files",
           side_effect=Exception("list error"))
    def test_show_files_list_error(self, *_):
        self.ctrl.show_files()

    @patch("smartbudget.core_module_2.file_io_data_controller.list_files", return_value=[])
    def test_show_files_empty(self, *_):
        self.ctrl.show_files()

    @patch("smartbudget.core_module_2.file_io_data_controller.list_files",
           return_value=["a.json", "records.json"])
    def test_show_files_normal(self, *_):
        self.ctrl.show_files()

    # =========================================================
    # delete_backup_file()
    # =========================================================
    @patch("builtins.input", return_value="")
    def test_delete_file_empty(self, *_):
        self.ctrl.delete_backup_file()

    @patch("builtins.input", return_value="records.json")
    def test_delete_file_block_system(self, *_):
        self.ctrl.delete_backup_file()

    @patch("builtins.input", return_value="file.json")
    @patch("smartbudget.core_module_2.file_io_data_controller.delete_file",
           side_effect=Exception("delete boom"))
    def test_delete_file_error(self, *_):
        self.ctrl.delete_backup_file()

    @patch("builtins.input", return_value="file.json")
    @patch("smartbudget.core_module_2.file_io_data_controller.delete_file", return_value=True)
    def test_delete_file_success(self, mock_delete, *_):
        self.ctrl.delete_backup_file()
        mock_delete.assert_called_once()

    @patch("builtins.input", return_value="file.json")
    @patch("smartbudget.core_module_2.file_io_data_controller.delete_file", return_value=False)
    def test_delete_file_not_found(self, *_):
        self.ctrl.delete_backup_file()

    @classmethod
    def tearDownClass(cls):
        print("[FileIO] tearDownClass\n")
