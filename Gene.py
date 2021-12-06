import numpy as np
from __future__ import annotations

class Gene:
    def __init__(self) -> None:
        self.gene = np.array([])
        self.fintess = 0

    def __lt__(self, gene2: Gene) -> bool:
        if self.fintess < gene2.fintess:
            return True
        return False

    def __le__(self, gene2: Gene) -> bool:
        if self.fintess <= gene2.fintess:
            return True
        return False

    def __eq__(self, gene2: Gene) -> bool:
        if self.fintess == gene2.fintess:
            return True
        return False

    def __ne__(self, gene2: Gene) -> bool:
        if self.fintess != gene2.fintess:
            return True
        return False

    def __gt__(self, gene2: Gene) -> bool:
        if self.fintess > gene2.fintess:
            return True
        return False

    def __ge__(self, gene2: Gene) -> bool:
        return not self < gene2