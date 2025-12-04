"""
Income class — stores positive money value with validation and normalization.
"""

from .base_record import RecordBase


class Income(RecordBase):
    """
    Represents a single income record.

    This class stores the name, amount (always positive), and source
    of the income. It provides validation, normalization, and property-
    based attribute access for robustness and consistency.
    """

    def __init__(self, name: str, amount: float, source: str):
        # ---- Validation ----
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Income name must be a non-empty string.")

        if not isinstance(amount, (int, float)):
            raise TypeError("Income amount must be numeric.")

        if amount <= 0:
            raise ValueError("Income amount must be positive.")

        if not isinstance(source, str) or not source.strip():
            raise ValueError("Income source must be a non-empty string.")

        # Call base class (RecordBase handles name + amount)
        super().__init__(name.strip(), float(abs(amount)))

        # ---- Normalize ----
        self._source = source.strip().lower()

    # --------------------------------------------------------
    # Properties — controlled access
    # --------------------------------------------------------
    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Source must be a non-empty string.")
        self._source = value.strip().lower()

    # --------------------------------------------------------
    # description
    # --------------------------------------------------------
    def describe(self) -> str:
        return (
            "Income Record\n"
            f"  Name   : {self.name}\n"
            f"  Source : {self.source}\n"
            f"  Amount : {self.amount:.2f}\n"
        )

    # --------------------------------------------------------
    # Serialization
    # --------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "type": "Income",
            "name": self.name,
            "amount": float(self.amount),
            "source": self.source,
        }
