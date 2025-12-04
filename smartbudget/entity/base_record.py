from smartbudget.entity.constants import Limits


class SmartBudgetError(Exception):
    """Custom error for SmartBudget."""
    pass


class RecordBase:
    """
    Minimal RecordBase implementation matching ALL unittest expectations.
    """

    def __init__(self, name, amount):
        self._name = None
        self._amount = None

        self.name = name
        self.amount = amount

    # -------------------------------------------------------
    # name (tests patch this property)
    # -------------------------------------------------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise SmartBudgetError("Name must be a string")
        if not value.strip():
            raise SmartBudgetError("Name cannot be empty")
        if len(value) > Limits.MAX_NAME_LEN:
            raise SmartBudgetError("Name too long")
        self._name = value

    # -------------------------------------------------------
    # amount (tests patch this property)
    # -------------------------------------------------------
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        try:
            value = float(value)
        except Exception:
            raise SmartBudgetError("Amount must be numeric")
        if value <= 0:
            raise SmartBudgetError("Amount must be > 0")
        self._amount = value

    # -------------------------------------------------------
    # show()
    # -------------------------------------------------------
    def show(self):
        try:
            return f"{self.name}: {self.amount:.2f}"
        except Exception as e:
            raise SmartBudgetError(f"Failed show: {e}")

    # -------------------------------------------------------
    # to_dict()
    # -------------------------------------------------------
    def to_dict(self):
        try:
            return {
                "type": self.__class__.__name__,
                "name": self.name,
                "amount": float(self.amount)
            }
        except Exception as e:
            raise SmartBudgetError(f"Failed to_dict: {e}")

    # -------------------------------------------------------
    # repr / str
    # -------------------------------------------------------
    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, amount={self.amount})"

    def __str__(self):
        return f"{self.name}: {self.amount:.2f}"
