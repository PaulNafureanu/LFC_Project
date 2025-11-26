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
    SIMBOL_VID = "*"  # pentru cuvantul vid λ

    def __init__(self) -> None:
        # multimea neterminalelor
        self.VN: Set[str] = set()
        # multimea terminalelor
        self.VT: Set[str] = set()
        # simbolul de start
        self.S: str | None = None
        # multimea de productii (reguli)
        self.productiile: List[Productie] = list()

    def citire(self, file_path: Path) -> None:
        """
        Primesti calea catre un fisier text in care este definita o gramatica.
        Si se citesc elementele din aceast fisier, dupa urmatoarele reguli:
        - prima linie: elementele din multimea neterminalelor VN.
        - a doua linie: elementele din multimea terminalelor VT.
        - a treia linie: simbolul de start S.
        - urmatoarele linii: o regula de productie per linie cu spatiu intre membrul stang si drep (eg: S abS).
        - nu exista linii goale.
        """

        # Se deschide fisierul text
        with file_path.open("r", encoding="utf-8") as f:
            # Se citeste linie cu linie pana la final
            for index, line in enumerate(f, start=1):
                line = line.strip()

                # Daca linia este goala, fisierul este formatat incorect
                if not line:
                    raise ValueError(
                        f"[Eroare de format] Linia {index} este goala in fisierul: {file_path}"
                    )

                # Se citesc elementele neterminale
                if index == 1:
                    self.VN = set(  # pyright: ignore[reportConstantRedefinition]
                        line.split()
                    )

                # Se citesc elementele terminale
                elif index == 2:
                    self.VT = set(  # pyright: ignore[reportConstantRedefinition]
                        line.split()
                    )

                # Se citeste elementul de start
                elif index == 3:
                    self.S = line  # pyright: ignore[reportConstantRedefinition]

                # Se citesc productiile pana la finalul fisierului
                else:
                    [left, right] = line.split()
                    productie = Productie(left, right)
                    self.productiile.append(productie)

    def verificare(self, should_print: bool = True) -> bool:
        """
        Verifica daca gramatica citita din fisierul text respecta regulile urmatoare:

        (1) VN ∩ VT = ∅
        (2) S ∈ VN
        (3) Pentru fiecare regulă, membrul stâng conține cel puțin un neterminal
        (4) Există cel puțin o producție care are în stânga doar S
        (5) Fiecare producție conține doar elemente din VN și VT

        Se verifica toate regulile si va returna True daca se respecta toate,
        False (cu afisarea unui mesaj pentru fiecare regula nerespectata) in caz contrar.
        """

        # Defineste un format de printare a mesajelor cand nu se respecta regulile
        def print_invalid_rule(*rule_msg: str):
            if should_print:
                print("Nu se respecta regula: ", *rule_msg)

        # Presupunem ca gramatica este deja valida si incercam sa o testam
        is_valid: bool = True

        # (1) Verifica daca exista elemente comune in ambele seturi
        common_elements_vn_vt = self.VN.intersection(self.VT)
        if common_elements_vn_vt:
            is_valid = False
            print_invalid_rule(
                f"(1) VN ∩ VT trebuie sa fie vid, dar avem {common_elements_vn_vt} in ambele seturi."
            )

        # (2) Verifica daca simbolul de start se afla in setul neterminalilor: S ∈ VN
        if self.S not in self.VN:
            is_valid = False
            print_invalid_rule(
                f"(2) S ∈ VN, adica simbolul de start trebuie sa fie un neterminal."
            )

        # Presupunem ca nu exista o productie cu membrul stang S si incercam sa gasim o asemenea productie
        is_there_a_left_with_S: bool = False

        # Definim VN ∪ VT
        vn_vt_union = self.VN.union(self.VT)

        # Iteram prin toate productiile
        for index, productie in enumerate(self.productiile, start=1):

            left = productie.left
            right = productie.right

            is_there_one_nonterminal_in_left: bool = False
            is_every_symbol_in_VN_VT: bool = True

            # Pentru fiecare simbol din membrul stang
            for symbol in left:
                #  Verificam daca este neterminal
                if symbol in self.VN:
                    is_there_one_nonterminal_in_left = True
                # Sau daca nu este nici neterminal, nici terminal (adica, in afara VN ∪ VT)
                elif symbol not in self.VT:
                    is_every_symbol_in_VN_VT = False

            # Pentru fiecare simbol din membrul drept
            for symbol in right:
                # Verificam daca este simbolul vid si
                if symbol == self.SIMBOL_VID:
                    continue
                # Daca este in multimi
                if symbol not in vn_vt_union:
                    is_every_symbol_in_VN_VT = False

            # (3) Verificam daca se respecta regula ca fiecare membru stang sa aiba un neterminal
            if not is_there_one_nonterminal_in_left:
                is_valid = False
                print_invalid_rule(
                    f"(3) Pentru fiecare regula, membrul stang trebuie sa contina cel putin un neterminal. A se vedea productia {index}"
                )
            # (5) Verificam daca se respecta regula ca fiecare productie sa contina doar simboluri din VN si VT
            if not is_every_symbol_in_VN_VT:
                is_valid = False
                print_invalid_rule(
                    f"(5) Fiecare productie trebuie sa contina doar elemente din VN si VT. A se vedea productia {index}."
                )
                break

            # (4) Verifica daca exista o productie cu membrul stand format doar din simbolul de start
            if self.S == left:
                is_there_a_left_with_S = True

        # Daca nu exista membru stang ca simbol de start, nu se respecta regula 4
        if not is_there_a_left_with_S:
            is_valid = False
            print_invalid_rule(
                f"(4) Trebuie sa existe cel putin o productie care are in stanga doar simbolul de start '{self.S}'"
            )
        # Returneaza True daca se respecta toate regulile, sau False daca cel putin o regula este nerespectata.
        return is_valid

    def afisare(self):
        """
        Afiseaza frumos gramatica la terminal.
        """

        # Transforma un set de string-uri intr-un mesaj gata de printare
        def set_to_str(seq: Set[str]):
            return " " + ", ".join(sorted(seq)) + " "

        print("\nSe afiseaza gramatica definita prin: ")
        print(f"VN := {{{set_to_str(self.VN)}}}")
        print(f"VT := {{{set_to_str(self.VT)}}}")
        print(f"S  := {self.S}")

        # Iterare si printare toate productiile
        print("\nProductii: ")
        for index, productie in enumerate(self.productiile, start=1):
            print(f"({index}) {productie}")

    def generare(self, should_print: bool = True) -> List[str]:
        """
        Genereaza un cuvant final incepand de la simbolul de start, cu afisarea fiecarui pas.
        Returneaza lista de pasi in ordine de la simbolul de start pana la cuvantul generat.

        Procesul de generare:
        - Se alege aleatoriu o regula de productie aplicabila.
        - Daca productia aleasa anterior poate fi aplicata in mai multe locuri in cuvant,
        atunci locul in care se va aplica va fi si el ales tot aleatoriu.
        - Se repeta pana cuvantul transformat este format doar din terminale.
        """

        intermediary_steps: List[str] = list()

        # Daca nu exista simbol de start returneaza o lista goala de pasi intermediari
        if not self.S:
            return intermediary_steps

        # Se initializeaza primul pas cu simbolul de start
        word_step = self.S
        intermediary_steps.append(word_step)

        # Se initializeaza o lista care va contine neterminalele cuvantului cu simbolul de start
        vn_symbols_in_word: List[str] = list(self.VN.intersection(word_step))

        # Se printeaza primul pas (S) daca se doreste
        if should_print:
            print(f"{word_step}", end="")

        # Cat timp exista neterminale in cuvant
        while vn_symbols_in_word:

            # Definim setul de productii aplicabile pe acest cuvant
            productii_aplicabile: Set[Productie] = set()
            for symbol in vn_symbols_in_word:
                for productie in self.productiile:
                    # prin compararea fiecarui simbol al cuvantului cu membrul stang al fiecarei productii din gramatica
                    if symbol == productie.left:
                        productii_aplicabile.add(productie)

            # In cazul in care nu exista productii aplicabile
            if not productii_aplicabile:
                # Se verifica daca la acest pas, cuvantul este format doar din terminale
                just_terminals: bool = set(word_step).issubset(self.VT)

                # Daca este, atunci iesire din ciclu. In caz contrar, ridica o eroare.
                if just_terminals:
                    break
                else:
                    raise ValueError(
                        f"[Eroare] Cuvantul '{word_step}' nu este format doar din terminale, dar nu exista productii aplicabile. A se verifica gramatica"
                    )

            # Se alege aleatoriu o productie
            prod_random = random.choice(list(productii_aplicabile))

            # Definim setul de pozitii posibile unde productia aleasa se poate aplica
            possible_positions: Set[int] = set()
            for index, symbol in enumerate(word_step):
                # prin comparare fiecarui simbol al cuvantului cu membrul stang al productiei alese
                if symbol == prod_random.left:
                    possible_positions.add(index)

            # Se alege aleatoriu o pozitie in cuvant
            pos_random = random.choice(list(possible_positions))

            # Se aplica productia prin inlocuirea simbolului cu membrul drept al productiei
            new_word_step: str = ""
            # Daca membrul drept este vid atunci se elimina simbolul de tot, altfel se inlocuieste
            if prod_random.right == self.SIMBOL_VID:
                new_word_step = word_step[:pos_random] + word_step[pos_random + 1 :]
            else:
                chars = list(word_step)
                chars[pos_random] = prod_random.right
                new_word_step = "".join(chars)

            # Se printeaza pas cu pas transformarile
            if should_print:
                print(f" ⟶ {new_word_step}", end="")

            # Se adauga noul cuvant format in lista finala
            intermediary_steps.append(new_word_step)

            # Si se reia procesul pana cand cuvantul este format doar din terminale, astfel spus len(vn_symbols_in_word) = 0
            word_step = new_word_step
            vn_symbols_in_word = list(self.VN.intersection(word_step))

        # Verificam daca cuvantul final este format doar din terminale. Daca nu ridicam o eroare.
        final_word = intermediary_steps[-1]
        if not set(final_word).issubset(self.VT):
            # Cum la iesirea din ciclu nu mai exista simboluri neterminale, atunci cuvantul final contine simboluri din afara VN ∪ VT
            raise ValueError(
                f"[Eroare] Cuvantul final '{final_word}' trebuie sa fie format din simboluri terminale. A se verifica gramatica."
            )

        # printeaza new line si returneaza lista de pasi generate de productii
        print()
        return intermediary_steps
