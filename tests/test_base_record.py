import unittest
import logging
from smartbudget.entity.base_record import RecordBase

logger = logging.getLogger(__name__)


class TestRecordBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("=== [TestRecordBase] Preparing class-level resources ===")
        cls.default_name = "Sample"
        cls.default_amount = 20

    def setUp(self):
        logger.debug("[TestRecordBase] setUp: Creating a fresh RecordBase instance")
        self.record = RecordBase(self.default_name, self.default_amount)

    def test_attributes(self):
        logger.debug("[TestRecordBase] Running test_attributes")
        self.assertEqual(self.record.name, "Sample")
        self.assertEqual(self.record.amount, 20)
        self.assertIsInstance(self.record.name, str)
        self.assertGreaterEqual(self.record.amount, 0)

    def test_to_dict(self):
        logger.debug("[TestRecordBase] Running test_to_dict")
        d = self.record.to_dict()
        self.assertIn("name", d)
        self.assertIn("amount", d)
        self.assertEqual(d["amount"], 20)
        self.assertIsInstance(d, dict)

    def tearDown(self):
        logger.debug("[TestRecordBase] tearDown: Clearing instance")
        self.record = None

    @classmethod
    def tearDownClass(cls):
        logger.info("=== [TestRecordBase] Class-level cleanup complete ===")
