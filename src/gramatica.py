from typing import List, Set
from pathlib import Path
import random


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

    def verificare(self) -> bool:
        print("\n")

        def print_invalid_msg(*rule_msg: str):
            print("Nu se respecta regula: ", *rule_msg)

        is_valid: bool = True

        VNset = set(self.VN)
        VTset = set(self.VT)

        # (1) Verifica daca exista simboluri comune si daca respecta regula: VN ∩ VT = {}
        common = VNset.intersection(VTset)
        if common:
            is_valid = False
            print_invalid_msg(
                f"(1) VN ∩ VT trebuie sa fie vid, dar avem {common} in ambele seturi."
            )

        # (2) Verifica daca simbolul de start se afla in setul neterminalilor: S ∈ VN
        if self.S not in VNset:
            is_valid = False
            print_invalid_msg(
                f"(2) S ∈ VN, simbolul de start trebuie sa fie un nonterminal."
            )

        is_left_with_S_only: bool = False

        for index, productie in enumerate(self.productiile, start=1):

            left = productie.left
            right = productie.right

            is_there_one_nonterminal_in_left: bool = False
            is_every_symbol_in_VN_VT: bool = True

            for symbol in left:
                if symbol in VNset:
                    is_there_one_nonterminal_in_left = True
                elif symbol not in VTset:
                    is_every_symbol_in_VN_VT = False

            for symbol in right:
                if symbol not in VNset.union(VTset):
                    is_every_symbol_in_VN_VT = False

            if not is_there_one_nonterminal_in_left:
                is_valid = False
                print_invalid_msg(
                    f"(3) Pentru fiecare regulă, membrul stâng conține cel puțin un neterminal. A se vedea productia {index}"
                )

            if not is_every_symbol_in_VN_VT:
                is_valid = False
                print_invalid_msg(
                    f"(5) Fiecare producție conține doar elemente din VN și VT. A se vedea productia {index}."
                )
                break

            # (4) Verifica daca exista o productie cu membrul stand format doar din simbolul de start
            if self.S == left:
                is_left_with_S_only = True

        if not is_left_with_S_only:
            is_valid = False
            print_invalid_msg(
                f"(4) Există cel puțin o productie care are in stanga doar simbolul de start '{self.S}'"
            )

        return is_valid

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
        if not self.S:
            return None

        word = self.S

        VNset = set(self.VN)
        vn_symbols_in_word: List[str] = list(self.S)

        print(f"{word}", end="")
        
        while vn_symbols_in_word:
            
            productii:Set[Productie] = set()
            for symbol in vn_symbols_in_word:
                for productie in self.productiile:
                    if symbol == productie.left:
                        productii.add(productie)
                        
            prod_picker = random.randint(0, len(productii) - 1)
            prod_random = list(productii)[prod_picker]
            
            possible_positions: Set[int] = set()
            for index, symbol in enumerate(word):
                if symbol == prod_random.left:
                    possible_positions.add(index)
            
            pos_picker = random.randint(0, len(possible_positions) - 1)
            pos_random = list(possible_positions)[pos_picker]
            
            chars = list(word)
            chars[pos_random] = prod_random.right
            
            print(f" ⟶ {"".join(chars)}", end="")
            word = "".join(chars)
            
            vn_symbols_in_word = list(VNset.intersection(word))
        
        print()

