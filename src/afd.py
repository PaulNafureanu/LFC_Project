from typing import List
from pathlib import Path


class Tranzitie:
    # Reprezintă o tranziție a automatului: δ(q, a) = q'
    def __init__(self, membrul_stang: str, simbol: str, membrul_drept: str) -> None:
        # starea din care plecăm (q)
        self.membrul_stang = membrul_stang
        # simbolul de pe muchie (a)
        self.simbol = simbol
        # starea în care ajungem (q')
        self.membrul_drept = membrul_drept

    def __str__(self) -> str:
        # Afișare prietenoasă a tranziției, sub forma δ(q, a) = q'
        return f"δ({self.membrul_stang}, {self.simbol}) = {self.membrul_drept}"


class AFD:
    """
    Clasa care modelează un Automat Finit Determinist.

    Atribute:
        Stari         - mulțimea stărilor (Q)
        Sigma         - alfabetul (Σ)
        Delta         - tipul tranziției (clasa Tranzitie)
        Reguli        - lista de tranziții efective (δ)
        StareInitiala - starea inițială (q0)
        StariFinale   - mulțimea stărilor finale (F)
    """

    def __init__(self) -> None:
        # Q - mulțimea stărilor
        self.Stari: List[str] = list()
        # Σ - alfabetul
        self.Sigma: List[str] = list()
        # Delta nu este o valoare, ci o referință la clasa Tranzitie (pentru a crea obiecte)
        self.Delta = Tranzitie
        # Lista de tranziții efective δ ⊆ Q × Σ × Q
        self.Reguli: List[Tranzitie] = list()
        # q0 - starea inițială (poate fi None până o citim din fișier)
        self.StareInitiala: str | None = None
        # F - mulțimea stărilor finale
        self.StariFinale: List[str] = list()

    def citire(self, file_path: Path):
        """
        Citește definiția AFD-ului dintr-un fișier text.

        Formatul așteptat (pe linii), conform convenției tale:
        1: lista stărilor (Q)
        2: starea inițială (q0)
        3: lista stărilor finale (F)
        4: alfabetul (Σ)
        5+: câte o tranziție pe linie: <stare_stânga> <simbol> <stare_dreapta>
        """
        with file_path.open("r", encoding="utf-8") as f:
            for index, line in enumerate(f, start=1):
                # Eliminăm spațiile de la început/sfârșit
                line = line.strip()

                # Dacă avem o linie complet goală, o considerăm eroare de format
                if not line:
                    raise ValueError(
                        f"[Eroare de format] Linia {index} este goala in fisierul: {file_path}"
                    )

                if index == 1:
                    # Linia 1: stările, separate prin spații
                    self.Stari = list(line.split())

                elif index == 2:
                    # Linia 2: starea inițială
                    self.StareInitiala = line

                elif index == 3:
                    # Linia 3: stările finale, separate prin spații
                    self.StariFinale = list(line.split())

                elif index == 4:
                    # Linia 4: alfabetul, simboluri separate prin spații
                    self.Sigma = list(line.split())

                else:
                    # Liniile 5+ conțin tranziții: q a q'
                    [stanga, simbol, dreapta] = line.split()
                    # Construim o tranziție folosind clasa Tranzitie
                    tranzitie = self.Delta(stanga, simbol, dreapta)
                    # Și o adăugăm în lista de reguli
                    self.Reguli.append(tranzitie)

    def validare(self, should_print: bool = True) -> bool:
        """
        Validează AFD-ul citit, conform condițiilor:
            - Q conține stări distincte
            - Σ este un alfabet valid (simboluri distincte, fiecare un singur caracter)
            - fiecare tranziție are: starea din Q, simbol din Σ și stare rezultată din Q
            - starea inițială este în Q
            - F este inclus în Q
        Returnează True dacă este valid, False în caz contrar.
        """
        este_valid: bool = True

        def print_invalid_rule(*rule_msg: str):
            # Funcție internă pentru a afișa mesaje de eroare doar dacă should_print este True
            if should_print:
                print("Nu se respecta regula: ", *rule_msg)

        # Verificăm unicitatea stărilor
        stari_set = set(self.Stari)

        if len(stari_set) != len(self.Stari):
            # Avem duplicate în Q
            este_valid = False
            print_invalid_rule(f"(1) Q trebuie sa contina stari distincte.")

        # Verificăm unicitatea simbolurilor din alfabet
        if len(set(self.Sigma)) != len(self.Sigma):
            este_valid = False
            print_invalid_rule(f"(2) Alfabetul sigma nu are simboluri distincte.")

        # Verificăm ca fiecare simbol să fie un singur caracter (simbol simplu)
        if not all(len(c) == 1 for c in self.Sigma):
            este_valid = False
            print_invalid_rule(f"(2) Alfabetul sigma nu are simboluri simple.")

        # Validăm fiecare tranziție din δ
        for index, tranzitie in enumerate(self.Reguli):
            # Verificăm membrul stâng (starea de plecare)
            if tranzitie.membrul_stang not in self.Stari:
                este_valid = False
                print_invalid_rule(
                    f"(3) In tranzitia {index} membrul stang nu este o stare in Q."
                )

            # Verificăm simbolul
            if tranzitie.simbol not in self.Sigma:
                este_valid = False
                print_invalid_rule(
                    f"(3) In tranzitia {index} simbolul nu se afla in alfabetul Sigma."
                )

            # Verificăm membrul drept (starea de sosire)
            if tranzitie.membrul_drept not in self.Stari:
                este_valid = False
                print_invalid_rule(
                    f"(3) In tranzitia {index} membrul drept nu este o stare in Q."
                )

        # Verificăm starea inițială
        if self.StareInitiala not in self.Stari:
            este_valid = False
            print_invalid_rule(f"(4) Starea initiala nu este din Q.")

        # Verificăm că F este inclus în Q
        if not set(self.StariFinale).issubset(set(self.Stari)):
            este_valid = False
            print_invalid_rule(f"(5) Starile finale F nu sunt stari incluse in Q.")

        return este_valid

    def afisare(self):
        """
        Afișează frumos componentele AFD-ului:
            - Q
            - Σ
            - q0
            - F
            - toate tranzițiile δ
        """

        def list_to_str(seq: List[str]):
            # Transformă o listă într-un string cu elemente sortate și separate prin virgulă
            return " " + ", ".join(sorted(seq)) + " "

        print("\nSe afiseaza AFD definita prin: ")
        print(f"Stari = {list_to_str(self.Stari)}")
        print(f"Sigma = {list_to_str(self.Sigma)}")

        print()
        print(f"Stare initiala = {self.StareInitiala}")
        print(f"Stari finale = {list_to_str(self.StariFinale)}")
        print("\nTranzitii:")

        # Afișăm fiecare tranziție pe o linie separată
        # Folosim comprehensiune ca să adăugăm un spațiu în față pentru format mai frumos
        print("\n".join({" " + str(r) for r in self.Reguli}))

    def verificare(self, cuvant: str):
        """
        Verifică dacă un cuvânt este:
            - "acceptat"    dacă se termină într-o stare finală
            - "neacceptat"  dacă se termină într-o stare care nu este finală
            - "blocaj"      dacă la un moment dat nu există tranziție definită
        În plus, afișează toate etapele prin care trece cuvântul.
        """
        # Eliminăm spațiile din jurul cuvântului
        cuvant = cuvant.strip()

        # Mai întâi verificăm dacă toate simbolurile din cuvânt sunt în alfabet
        for c in cuvant:
            if c not in self.Sigma:
                # Afișăm mesaj corespunzător pentru simbol invalid
                print(
                    f"simbol invalid '{c}' in cuvant. "
                    f"Alfabetul este {{{', '.join(self.Sigma)}}}"
                )
                return "neacceptat"

        # Pornim din starea inițială
        print(f"Stare initiala: {self.StareInitiala}")
        stare_curenta = self.StareInitiala

        # Parcurgem cuvântul simbol cu simbol
        for simbol in cuvant:
            print(simbol)  # Afișăm simbolul curent
            exista_regula = False

            # Căutăm o tranziție definită din starea curentă cu simbolul curent
            for regula in self.Reguli:
                if regula.membrul_stang == stare_curenta and regula.simbol == simbol:
                    exista_regula = True
                    # Afișăm tranziția efectuată
                    print(f"{stare_curenta} --{simbol}--> {regula.membrul_drept}")
                    # Trecem în noua stare
                    stare_curenta = regula.membrul_drept
                    break

            # Dacă nu s-a găsit nicio tranziție, automatul se blochează
            if not exista_regula:
                print(
                    f"Blocaj: nu exista tranzitie din {stare_curenta} cu simbol {simbol}"
                )
                return "blocaj"

        # După ce am citit tot cuvântul, verificăm în ce stare am ajuns
        print(f"Stare finala dupa citirea intregului cuvant: {stare_curenta}")
        if stare_curenta in self.StariFinale:
            print("Cuvant acceptat")
            return "acceptat"
        else:
            print("Cuvant neacceptat")
            return "neacceptat"
