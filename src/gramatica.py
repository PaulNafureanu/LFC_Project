from typing import Set
from pathlib import Path


class Productie:
    def __init__(self, left: str, right: str) -> None:
        # Membrul stang al regulii de productie
        self.left: str = left
        # Membrul drept al regulii de productie
        self.right: str = right


class Gramatica:
    def __init__(self) -> None:
        # multimea neterminalelor
        self.VN: Set[str] = set()
        # multimea terminalelor
        self.VT: Set[str] = set()
        # simbolul de start
        self.S: str | None = None
        # multimea de productii (reguli)
        self.productiile: Set[Productie] = set()

    def citire(self, file_path: Path):
        pass

    def verificare(self):
        pass

    def afisare(self):
        pass

    def generare(self):
        pass
