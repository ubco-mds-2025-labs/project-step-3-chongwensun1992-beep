import os
import json
import shutil
import unittest
from smartbudget.file_io_module_3 import json_io
from smartbudget.entity.income import Income
from smartbudget.entity.expense import Expense
from smartbudget.entity.base_record import RecordBase


class TestJsonIO(unittest.TestCase):

    TEST_DIR = "files"
    TEST_FILE = "records.json"

    def setUp(self):
        """Clean files/ directory before each test."""
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)
        os.makedirs(self.TEST_DIR, exist_ok=True)

    def tearDown(self):
        """Remove files directory after each test."""
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)

    # ----------------------------
    # save_to_json()
    # ----------------------------
    def test_save_to_json(self):
        records = [
            Income("Salary", 3000, "Work"),
            Expense("Food", 50, "Daily"),
        ]

        json_io.save_to_json(records, self.TEST_FILE)

        path = os.path.join(self.TEST_DIR, self.TEST_FILE)
        self.assertTrue(os.path.exists(path))

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["type"], "Income")
        self.assertEqual(data[1]["type"], "Expense")

    # ----------------------------
    # load_from_json: file not exist
    # ----------------------------
    def test_load_from_json_when_file_missing(self):
        """File does not exist → should create empty JSON file + return empty list"""
        path = os.path.join(self.TEST_DIR, self.TEST_FILE)
        self.assertFalse(os.path.exists(path))

        result = json_io.load_from_json(self.TEST_FILE)

        # Should return an empty list
        self.assertEqual(result, [])

        # Should create empty JSON file
        self.assertTrue(os.path.exists(path))

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, [])

    # ----------------------------
    # load_from_json: restore Income / Expense / RecordBase
    # ----------------------------
    def test_load_from_json_restore_objects(self):
        sample = [
            {"type": "Income", "name": "Salary", "amount": 3000, "source": "Work"},
            {"type": "Expense", "name": "Food", "amount": -50, "category": "Daily"},
            {"type": "Other", "name": "Misc", "amount": 10},
        ]

        path = os.path.join(self.TEST_DIR, self.TEST_FILE)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sample, f, indent=4)

        records = json_io.load_from_json(self.TEST_FILE)

        self.assertEqual(len(records), 3)
        self.assertIsInstance(records[0], Income)
        self.assertIsInstance(records[1], Expense)
        self.assertIsInstance(records[2], RecordBase)

        self.assertEqual(records[0].name, "Salary")
        self.assertEqual(records[1].amount, 50)   # Expense should convert to positive via abs()

    # ----------------------------
    # append_to_json()
    # ----------------------------
    def test_append_to_json(self):
        json_io.save_to_json([Income("A", 100, "X")], self.TEST_FILE)

        json_io.append_to_json([Expense("B", 20, "Food")], self.TEST_FILE)

        path = os.path.join(self.TEST_DIR, self.TEST_FILE)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[1]["type"], "Expense")

    # ----------------------------
    # clear_json()
    # ----------------------------
    def test_clear_json(self):
        json_io.save_to_json([Income("X", 100, "Y")], self.TEST_FILE)

        result = json_io.clear_json(self.TEST_FILE)

        self.assertTrue(result)

        path = os.path.join(self.TEST_DIR, self.TEST_FILE)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data, [])

