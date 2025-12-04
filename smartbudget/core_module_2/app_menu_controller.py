"""
SmartBudget CLI Application Interface
-------------------------------------
"""

# ------------------ Imports ------------------ #

from smartbudget.core_module_2.budget_record_controller import BudgetRecordController
from smartbudget.core_module_2.file_io_data_controller import FileIoDataStorageController


# ------------------ Create Controller Instances ------------------ #

rec = BudgetRecordController()
sys = FileIoDataStorageController()


# ------------------ UI Menu ------------------ #

def print_menu():
    print("====================================")
    print("       SmartBudget Main Menu        ")
    print("====================================")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. Show Summary")
    print("4. Show Expense Details")
    print("5. Show Income Details")
    print("6. Backup Records to JSON")
    print("7. List Backup Files")
    print("8. Delete Backup File")
    print("9. Reset Records")
    print("10. Show Expense Chart")
    print("0. Exit")
    print("====================================")


# ------------------ Main Application Loop ------------------ #

def run():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            rec.add_income()
        elif choice == "2":
            rec.add_expense()
        elif choice == "3":
            rec.show_summary()
        elif choice == "4":
            rec.show_expense_details()
        elif choice == "5":
            rec.show_income_details()
        elif choice == "6":
            sys.save_data()
        elif choice == "7":
            sys.show_files()
        elif choice == "8":
            sys.delete_backup_file()
        elif choice == "9":
            sys.clear_data()
        elif choice == "10":
            rec.show_expense_plot()
        elif choice == "0":
            print("\nExiting SmartBudget. Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice. Try again.\n")
