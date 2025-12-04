"""
FileIoDataStorageController
---------------------------

Controller class responsible for all SYSTEM-LEVEL data storage
operations in SmartBudget.

This includes:
    • Saving current records to a backup JSON file
    • Loading records from backup files
    • Clearing the system's primary data store (records.json)
    • Listing user-created backup files
    • Deleting selected backup files

Acts as the STORAGE CONTROLLER layer, bridging:
    - entity models (Income, Expense)
    - low-level file I/O helper functions in file_io_module_3
"""

from smartbudget.entity.income import Income
from smartbudget.entity.expense import Expense

from smartbudget.file_io_module_3 import (
    save_to_json,
    load_from_json,
    file_exists,
    list_files,
    delete_file,
    clear_json,
)


class FileIoDataStorageController:
    """High-level controller for SmartBudget's file-based storage operations."""

    # --------------------------------------------------------
    # Clear primary data file
    # --------------------------------------------------------
    def clear_data(self):
        confirm = input("⚠ Are you sure you want to CLEAR ALL DATA? (y/n): ").lower()
        if confirm == "y":
            clear_json()  # Resets records.json
            print("✔ All records have been cleared.\n")
        else:
            print("❌ Cancelled.\n")

    # --------------------------------------------------------
    # Save current records to user-specified file
    # --------------------------------------------------------
    def save_data(self):
        filename = input("Enter filename to save (e.g., backup.json): ").strip()

        if filename == "records.json":
            print("❌ Cannot save to system file.\n")
            return

        if file_exists(filename):
            overwrite = input("⚠ File exists. Overwrite? (y/n): ").lower()
            if overwrite != "y":
                print("❌ Save cancelled.\n")
                return

        data = load_from_json("records.json")
        save_to_json(data, filename)

        print(f"✔ Records saved to {filename}\n")

    # --------------------------------------------------------
    # Load backup file into memory
    # --------------------------------------------------------
    def load_data(self, incomes: list, expenses: list):
        """
        Loads records from a backup file and appends them into
        the provided incomes/expenses lists.
        """

        filename = input("Enter filename to load: ").strip()

        if not file_exists(filename):
            print("❌ File not found.\n")
            return

        loaded_records = load_from_json(filename)

        for record in loaded_records:
            if isinstance(record, Income):
                incomes.append(record)
            elif isinstance(record, Expense):
                expenses.append(record)

        print(f"\n✔ Loaded {len(loaded_records)} records from '{filename}'\n")
        for rec in loaded_records:
            print(" -", rec.describe())
        print()

    # --------------------------------------------------------
    # Display available backup files
    # --------------------------------------------------------
    def show_files(self):
        print("\nFiles in 'files/' directory:")

        files = [f for f in list_files() if f != "records.json"]

        if not files:
            print(" (No user files found)")
        else:
            for f in files:
                print(" -", f)
        print()

    # --------------------------------------------------------
    # Delete user-selected backup file
    # --------------------------------------------------------
    def delete_backup_file(self):
        filename = input("Enter filename to delete: ").strip()

        if filename == "records.json":
            print("❌ Cannot delete system file.\n")
            return

        if delete_file(filename):
            print(f"✔ Deleted '{filename}'\n")
        else:
            print("❌ File not found.\n")
