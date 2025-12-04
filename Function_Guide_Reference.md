# SmartBudget — FUNCTIONS.md (Final Version)

This document outlines every module, class, and function within the SmartBudget package, providing a clear reference for structure and behavior. It supports transparency for reviewers, improves long-term maintainability, and ensures the project is fully prepared for evaluation.

------------------------------------------------------------
PACKAGE STRUCTURE OVERVIEW
------------------------------------------------------------

SmartBudget includes four functional areas:


1. entity/ — financial data models  
2. analysis/ — summaries, insights, charts  
3. core/ — controllers and CLI interaction  
4. io/ — JSON persistence and file utilities


------------------------------------------------------------
1. ENTITY MODULES (smartbudget/entity/)
------------------------------------------------------------

base_record.py
---------------
Class: RecordBase  
Parent class of Income and Expense.

Attributes:
- name: record label  
- amount: validated numeric amount  
- timestamp: creation time

Methods:
- __init__(name, amount)  
- _validate_name(name)  
- _validate_amount(amount)  
- show()  
- to_dict(): base serialization

constants.py
-------------
Class: Limits  
Attributes:
- MAX_AMOUNT  
- MAX_NAME_LEN  

income.py
----------
Class: Income  
Represents positive income.

Methods:
- __init__(name, amount, source)  
- describe()  
- to_dict(): includes type="Income" and source

expense.py
-----------
Class: Expense  
Represents positive expense value.

Methods:
- __init__(name, amount, category)  
- describe()  
- to_dict(): includes type="Expense" and category

------------------------------------------------------------
2. ANALYSIS MODULES (smartbudget/analysis/)
------------------------------------------------------------

insights.py
------------
Functions:
- _load_split(): loads JSON, returns (incomes, expenses)
- income_details(): formatted strings of incomes
- expense_details(): formatted strings of expenses
- plot_expense_by_category(): bar chart of expenses

summary.py
-----------
Functions:
- total_income(): sum of all income amounts  
- total_expenses(): sum of all expense amounts  
- budget_balance(): total_income - total_expenses  
- summary_dict(): returns {"income": x, "expenses": y, "balance": z}

------------------------------------------------------------
3. CONTROLLER MODULES (smartbudget/core/)
------------------------------------------------------------

budget_record_controller.py
----------------------
Functions:
- add_income(): input → Income object → save  
- add_expense(): input → Expense object → save  
- show_summary(): prints totals and balance  
- show_income_details()  
- show_expense_details()  
- show_expense_chart(): calls plot_expense_categories()

file_io_data_controller.py
---------------------
Functions:
- save_data(): save current records.json as backup  
- clear_data(): reset main JSON  
- load_data(incomes, expenses): rebuild objects  
- show_files(): list backup files  
- delete_backup_file(): remove a selected file  

app_menu_controller.py
-------------------
Functions:
- print_menu(): prints menu including chart option  
- run(): main loop dispatching actions  

------------------------------------------------------------
4. IO MODULES (smartbudget/io/)
------------------------------------------------------------
The IO layer in SmartBudget manages JSON persistence and general file-handling.
It is responsible for saving, loading, validating, and maintaining data stored in the /files/ directory.

json_io.py
-----------
Functions:
- save_to_json(records, filename) 
  Serializes a list of Income/Expense objects and writes the result to a JSON file.
  
- append_to_json(records)  
  Loads the existing JSON file, appends a new record, and saves it back.
  
- load_from_json(filename): reconstruct Income or Expense by type  
  Reads a JSON file and reconstructs the corresponding Income and Expense objects based on the "type" field.
  
- clear_json(filename)
  Resets a JSON file by overwriting it with an empty list.
  
file_utils.py
--------------
Functions:
- file_exists(filename)  
  Checks whether a specified file exists in the /files/ directory.
  
- list_files() 
  Returns a list of all JSON backup files stored under /files/.
  
- delete_file(filename)
  Removes the selected JSON file from the backup directory.

------------------------------------------------------------
5. MAIN PROGRAM (main.py)
------------------------------------------------------------

Function:
- main(): starts the program via controller_menu.run()

------------------------------------------------------------
6. EXTENDED FEATURES (v2.0+)
------------------------------------------------------------

- Positive-amount Expense logic  
- Category-based bar chart visualization  
- Category grouping utilities  
- Summary dictionary for API/testing  
- Clean split into separate Income/Expense classes  
- Enhanced controller complexity  
- More modular structure for grading and maintainability

------------------------------------------------------------
SUMMARY
------------------------------------------------------------

SmartBudget provides:
- Clean OOP architecture  
- Modular design  
- JSON persistence  
- CLI-based interaction  
- Analytical summaries  
- Visual charts  
- Professional documentation


