"""
BudgetRecordController — Test-Compatible Version
Matches Step 3 tests exactly.
"""

from smartbudget.entity.base_record import SmartBudgetError


class BudgetRecordController:
    """Controller wrapper used by the tests."""

    def __init__(self):
        # tests patch this object!
        self.rec = None

    # ----------------------------------------------------
    # Summary
    # ----------------------------------------------------
    def show_summary(self):
        """
        Tests expect:
            - call self.rec.summary()
            - if self.rec.summary() raises → SmartBudgetError
        """
        try:
            return self.rec.summary()
        except Exception:
            raise SmartBudgetError("Failed to show summary")

    # ----------------------------------------------------
    # Income details
    # ----------------------------------------------------
    def show_income_details(self):
        """
        Tests expect:
            - if rec.incomes is empty → raise SmartBudgetError
            - else call rec.income_details()
            - if rec.income_details() raises → SmartBudgetError
        """
        try:
            if not getattr(self.rec, "incomes", []):
                raise SmartBudgetError("No incomes")

            return self.rec.income_details()

        except SmartBudgetError:
            raise
        except Exception:
            raise SmartBudgetError("Failed to show income details")

    # ----------------------------------------------------
    # Expense details
    # ----------------------------------------------------
    def show_expense_details(self):
        """
        Tests expect identical behavior to income:
            - raise SmartBudgetError if no rec.expenses
            - call rec.expense_details()
        """
        try:
            if not getattr(self.rec, "expenses", []):
                raise SmartBudgetError("No expenses")

            return self.rec.expense_details()

        except SmartBudgetError:
            raise
        except Exception:
            raise SmartBudgetError("Failed to show expense details")

    # ----------------------------------------------------
    # Expense plot
    # ----------------------------------------------------
    def show_expense_plot(self):
        """
        Tests expect:
            - MUST call rec.plot_expense_by_category()
            - if it raises → SmartBudgetError
        """
        try:
            return self.rec.plot_expense_by_category()

        except Exception:
            raise SmartBudgetError("Failed to show expense plot")
