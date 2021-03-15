from dataclasses import dataclass
from typing import Callable


@dataclass
class Rule:
    column: str
    rule: Callable
    description: str
