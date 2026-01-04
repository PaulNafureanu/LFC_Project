from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple, Set, Optional

Stare = str
Simbol = str

@dataclass(frozen=True)
class Tranzitie:
    """
    Reprezintă o singură regulă a automatului:
        q --a--> p
    (Atenție: În AFN, funcția δ(q, a) produce o mulțime de stări,
     dar o regulă individuală tot e "q, a -> p".)
    """
    membrul_stang: Stare
    simbol: Simbol
    membrul_drept: Stare

    def __str__(self) -> str:
        return f"δ({self.membrul_stang}, {self.simbol}) = {self.membrul_drept}"


class AFN:
    """
    AFN definit ca:
        M = (Q, Σ, δ, q0, F)
    - Q: stări (lista, păstrăm ordinea din fișier)
    - Σ: alfabet (lista)
    - δ: dict care mapează (q, a) -> set(stări)
    - q0: stare inițială
    - F: stări finale
    """

    def __init__(self) -> None:
        self.Stari: List[Stare] = []
        self.Sigma: List[Simbol] = []

        # δ: Q × Σ -> P(Q)
        # deci (q, a) -> {p1, p2, ...}
        self.Delta: Dict[Tuple[Stare, Simbol], Set[Stare]] = {}

        # Opțional: păstrăm și regulile individuale pentru afișare / validare ușoară
        self.Reguli: List[Tranzitie] = []

        self.StareInitiala: Optional[Stare] = None
        self.StariFinale: List[Stare] = []

    def adauga_tranzitie(self, q: Stare, a: Simbol, p: Stare) -> None:
        # Validări de bază (pe baza listelor citite)
        if q not in self.Stari or p not in self.Stari:
            raise ValueError("Starile trebuie sa existe in Q pentru a adauga o tranzitie.")
        if a not in self.Sigma:
            raise ValueError("Simbolul trebuie sa fie in alfabetul Sigma pentru a adauga o tranzitie.")

        t = Tranzitie(q, a, p)
        self.Reguli.append(t)

        # Actualizăm δ(q, a) (mulțime de stări)
        self.Delta.setdefault((q, a), set()).add(p)

    def citire(self, file_path: Path) -> None:
        """
        Format fișier (din ce ai scris tu):
        1) linia 1: stările (separate prin spațiu)
        2) linia 2: starea inițială
        3) linia 3: stările finale
        4) linia 4: alfabetul
        5+) tranziții: <stanga> <simbol> <dreapta>
        """
        with file_path.open("r", encoding="utf-8") as f:
            for index, raw_line in enumerate(f, start=1):
                line = raw_line.strip()

                # Dacă vrei STRICT fără linii goale, păstrează raise.
                # Dacă accepți linii goale, înlocuiește cu `continue`.
                if not line:
                    raise ValueError(
                        f"[Eroare de format] Linia {index} este goala in fisierul: {file_path}"
                    )

                if index == 1:
                    self.Stari = line.split()

                elif index == 2:
                    self.StareInitiala = line

                elif index == 3:
                    self.StariFinale = line.split()

                elif index == 4:
                    self.Sigma = line.split()

                else:
                    parts = line.split()
                    if len(parts) != 3:
                        raise ValueError(
                            f"[Eroare de format] Linia {index} trebuie sa aiba 3 campuri: "
                            f"<stanga> <simbol> <dreapta>. Gasit: {parts}"
                        )
                    stanga, simbol, dreapta = parts
                    self.adauga_tranzitie(stanga, simbol, dreapta)

    def validare(self, should_print: bool = True) -> bool:
        """
        Verifică:
        (1) Q: stări distincte
        (2) Σ: simboluri distincte (+ simbol simplu dacă asta cere cursul)
        (3) Tranzițiile folosesc doar elemente din Q și Σ
        (4) q0 ∈ Q
        (5) F ⊆ Q
        """
        este_valid = True

        def print_invalid_rule(*rule_msg: str) -> None:
            if should_print:
                print("Nu se respecta regula: ", *rule_msg)

        # (1) Q distinct
        if len(set(self.Stari)) != len(self.Stari):
            este_valid = False
            print_invalid_rule("(1) Q trebuie sa contina stari distincte.")

        # (2) Sigma distinct
        if len(set(self.Sigma)) != len(self.Sigma):
            este_valid = False
            print_invalid_rule("(2) Alfabetul Sigma nu are simboluri distincte.")

        # (2) simbol simplu (dacă așa cere cursul)
        if not all(len(c) == 1 for c in self.Sigma):
            este_valid = False
            print_invalid_rule("(2) Alfabetul Sigma nu are simboluri simple (un singur caracter).")

        # (3) Validăm regulile
        for idx, t in enumerate(self.Reguli, start=1):
            if t.membrul_stang not in self.Stari:
                este_valid = False
                print_invalid_rule(f"(3) In tranzitia {idx} membrul stang nu este o stare in Q.")
            if t.simbol not in self.Sigma:
                este_valid = False
                print_invalid_rule(f"(3) In tranzitia {idx} simbolul nu se afla in alfabetul Sigma.")
            if t.membrul_drept not in self.Stari:
                este_valid = False
                print_invalid_rule(f"(3) In tranzitia {idx} membrul drept nu este o stare in Q.")

        # (4) q0
        if self.StareInitiala is None or self.StareInitiala not in self.Stari:
            este_valid = False
            print_invalid_rule("(4) Starea initiala nu este din Q.")

        # (5) F ⊆ Q
        if not set(self.StariFinale).issubset(set(self.Stari)):
            este_valid = False
            print_invalid_rule("(5) Starile finale F nu sunt stari incluse in Q.")

        return este_valid

    def afisare(self) -> None:
        """Afișează componentele AFN-ului: Q, Σ, q0, F și tranzițiile."""
        def list_to_str(seq: List[str]) -> str:
            return " " + ", ".join(sorted(seq)) + " "

        print("\nSe afiseaza AFN definita prin: ")
        print(f"Stari = {list_to_str(self.Stari)}")
        print(f"Sigma = {list_to_str(self.Sigma)}")
        print()
        print(f"Stare initiala = {self.StareInitiala}")
        print(f"Stari finale = {list_to_str(self.StariFinale)}")
        print("\nTranzitii:")

        # păstrăm ordinea și duplicatele (dacă există) exact cum s-au citit
        print("\n".join([" " + str(r) for r in self.Reguli]))
        
    
