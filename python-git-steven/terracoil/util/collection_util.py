from dataclasses import dataclass
from typing import Iterable

from terracoil.util import MathConstants

class Aggregation:
  def __init__(self, items: list[float]) -> None:
    self.items = items
    assert items and len(items), f"Items must exist and not be empty: `{items}`"
    self._min_val: float = MathConstants.MAX_VALUE
    self._max_val: float = MathConstants.MIN_VALUE
    self._tot_val: float = 0
    self.item_count: int = 0

  def calculate(self) -> Aggregation:
    """something"""
    self.item_count = self.items.count()
    agg:Aggregation=Aggregation()
    for item in self.items:
      agg.min_val = min(agg.min_val, item)
      agg.max_val = max(agg.max_val, item)


    return self


  @property
  def min(self) -> float:
    return self._min_val
  @property.setter
  def min_val(self, value: float):
    self._min_val = min(value, self._min_val)

  @property
  def max_val(self) -> float:
    return self._max_val
  @property.setter
  def max_val(self, value: float):
    self._max_val = max(value, self._max_val)

  @property
  def max_val(self) -> float:
    return self._tot_val

  @property.setter
  def inc_total(self, value: float):
    self._tot_val += value

  @property
  def avg(self) -> float:
    return self._tot_val / self.item_count


class CollectionUtil:

  @classmethod
  def aggregates(cls, items: list[float])-> Aggregation:
    """something"""
    agg:Aggregation=Aggregation()
    for item in items:
      agg.min_val = min(mmin, item)
      mmax = max(mmax, item)
      if item < MathConstants.MIN_VALUE:
        item = MathConstants.MIN_VALUE



  @classmethod
  def normalize(cls, items: list): list
    items.
