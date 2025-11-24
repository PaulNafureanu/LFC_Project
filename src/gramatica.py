from typing import List
from pathlib import Path


class Productie:
    def __init__(self, left: str, right: str) -> None:
        # Membrul stang al regulii de productie
        self.left: str = left
        # Membrul drept al regulii de productie
        self.right: str = right

    def __str__(self) -> str:
        return f"{self.left} ⟶ {self.right}"


class Gramatica:
    SIMBOL_VID = "λ"
    
    def __init__(self) -> None:
        # multimea neterminalelor
        self.VN: List[str] = list()
        # multimea terminalelor
        self.VT: List[str] = list()
        # simbolul de start
        self.S: str | None = None
        # multimea de productii (reguli)
        self.productiile: List[Productie] = list()

    def citire(self, file_path: Path):

        with file_path.open("r", encoding="utf-8") as f:
            for index, line in enumerate(f, start=1):
                line = line.strip()

                if index == 1:
                    self.VN = list(line.split())  # type: ignore

                elif index == 2:
                    self.VT = list(line.split())  # type: ignore

                elif index == 3:
                    self.S = line  # type: ignore

                else:
                    [left, right] = line.split()
                    productie = Productie(left, right)
                    self.productiile.append(productie)

    def verificare(self):
        pass

    def afisare(self):

        def list_to_format(seq: List[str]):
            return " " + ", ".join(sorted(seq)) + " "

        print("\nSe afiseaza grafica definita prin: ")
        print(f"VN := {{{list_to_format(self.VN)}}}")
        print(f"VT := {{{list_to_format(self.VT)}}}")
        print(f"S  := {self.S}")
        print("\nProductii: ")
        for index, productie in enumerate(self.productiile, start=1):
            print(f"({index}) {productie}")

    def generare(self):
        pass
