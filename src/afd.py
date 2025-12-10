from typing import List
from pathlib import Path


class Tranzitie:
    def __init__(self, membrul_stang: str, simbol: str, membrul_drept: str) -> None:
        self.membrul_stang = membrul_stang
        self.simbol = simbol
        self.membrul_drept = membrul_drept

    def __str__(self) -> str:
        return f"δ({self.membrul_stang}, {self.simbol}) = {self.membrul_drept}"


class AFD:

    def __init__(self) -> None:
        self.Stari: List[str] = list()
        self.Sigma: List[str] = list()
        self.Delta = Tranzitie
        self.Reguli: List[Tranzitie] = list()
        self.StareInitiala: str | None = None
        self.StariFinale: List[str] = list()

    def citire(self, file_path: Path):
        with file_path.open("r", encoding="utf-8") as f:
            for index, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    raise ValueError(
                        f"[Eroare de format] Linia {index} este goala in fisierul: {file_path}"
                    )

                if index == 1:
                    self.Stari = list(line.split())

                elif index == 2:
                    self.StareInitiala = line

                elif index == 3:
                    self.StariFinale = list(line.split())

                elif index == 4:
                    self.Sigma = list(line.split())

                else:
                    [stanga, simbol, dreapta] = line.split()
                    tranzitie = self.Delta(stanga, simbol, dreapta)
                    self.Reguli.append(tranzitie)

    def validare(self, should_print: bool = True) -> bool:
        este_valid: bool = True

        def print_invalid_rule(*rule_msg: str):
            if should_print:
                print("Nu se respecta regula: ", *rule_msg)

        stari_set = set(self.Stari)

        if len(stari_set) != len(self.Stari):
            este_valid = False
            print_invalid_rule(f"(1) Q trebuie sa contina stari distincte.")

        if len(set(self.Sigma)) != len(self.Sigma):
            este_valid = False
            print_invalid_rule(f"(2) Alfabetul sigma nu are simboluri distincte.")

        if not all(len(c) == 1 for c in self.Sigma):
            este_valid = False
            print_invalid_rule(f"(2) Alfabetul sigma nu are simboluri simple.")

        for index, tranzitie in enumerate(self.Reguli):
            # A se face exceptie cu Q
            if tranzitie.membrul_stang not in self.Stari:
                este_valid = False
                print_invalid_rule(
                    f"(3) In tranzitia {index} membrul stang nu este o stare in Q."
                )

            if tranzitie.simbol not in self.Sigma:
                este_valid = False
                print_invalid_rule(
                    f"(3) In tranzitia {index} simbolul nu se afla in alfabetul Sigma."
                )

            if tranzitie.membrul_drept not in self.Stari:
                este_valid = False
                print_invalid_rule(
                    f"(3) In tranzitia {index} membrul drept nu este o stare in Q."
                )

        if self.StareInitiala not in self.Stari:
            este_valid = False
            print_invalid_rule(f"(4) Starea initiala nu este din Q.")

        if not set(self.StariFinale).issubset(set(self.Stari)):
            este_valid = False
            print_invalid_rule(f"(5) Starile finale F nu sunt stari incluse in Q.")

        return este_valid

    def afisare(self):

        def list_to_str(seq: List[str]):
            return " " + ", ".join(sorted(seq)) + " "

        print("\nSe afiseaza AFD definita prin: ")
        print(f"Stari = {list_to_str(self.Stari)}")
        print(f"Sigma = {list_to_str(self.Sigma)}")
        
        print()
        print(f"Stare initiala = {self.StareInitiala}")
        print(f"Stari finale = {list_to_str(self.StariFinale)}")
        print("\nTranzitii:")
        print(f"{"\n".join({" " + str(r) for r in  self.Reguli})}")

    def verificare(self, cuvant: str):
        
        for c in cuvant:
            if c not in self.Sigma:
                print(f"simbol invalid '{c} in cuvant. ", f"Alfabetul este {{{", ".join(self.Sigma)}}}")
                return "neacceptat"
            
        print(f"Stare initiala: {self.StareInitiala}")
        stare_curenta = self.StareInitiala
        
        for simbol in cuvant:
            exista_regula = False
            for regula in self.Reguli:
                if regula.membrul_stang == stare_curenta and regula.simbol == simbol:
                    exista_regula = True
                    print(f"{stare_curenta} --{simbol}--> {regula.membrul_drept}")
                    stare_curenta = regula.membrul_drept
            
            if not exista_regula:
                print(f"Blocaj: nu exista tranzitie din {stare_curenta} cu simbol {simbol}")
                return "blocaj"
            
        print(f"Stare finala dupa citirea intregului cuvant: {stare_curenta}")
        if stare_curenta in self.StariFinale:
            print("Cuvant acceptat")
            return "acceptat"
        else:
            print("Cuvant neacceptat")
            return "neacceptat"
