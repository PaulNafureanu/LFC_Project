from src.gramatica import Gramatica
from src.afd import AFD
from src.afn import AFN
from src.path import PathMaker
from typing import Set


def run_exercise_1_solution():
    """
    Ruleaza solutia pentru exercitiul 1
    """

    # Se defineste calea pentru fisierul care contine gramatica, independent de sistemul de operare.
    # Se poate incerca si cu alte fisiere, unde "2.txt" contine o gramatica invalida, iar "1.txt" si "3.txt" contin gramatici valide.
    path_maker = PathMaker(__file__, "data", "gramatica")
    file_path = path_maker.get_independent_OS_path("3.txt")

    # Definim un obiect de tip Gramatica
    G1 = Gramatica()

    # Se citeste din fisier o gramatica
    try:
        G1.citire(file_path)
    except Exception as e:
        print(e)
        return

    # Se verifica daca gramatica este valida. Si in cazul in care este, se afiseaza si se genereaza cuvintele
    if G1.verificare():
        G1.afisare()

        # Se defineste un set care va contine n cuvinte finale distincte generate de gramatica
        final_distinct_words: Set[str] = set()
        n = int(input("\nIntroduce-ti numarul de cuvinte de generat: "))

        # Pentru a evita cazul unei bucle infinite definim un maxim rezonabil de incercari
        attempt = 0
        LOOP_MAX_ATTEMPTS = 100_000

        # Se ruleaza functia de generare pana avem n cuvinte finale distincte
        while len(final_distinct_words) < n and attempt < LOOP_MAX_ATTEMPTS:
            attempt += 1
            try:
                steps = G1.generare()
            except Exception as e:
                print(e)
                continue

            # Daca nu exista pasi intermediari (lista e goala), treci la urmatoare incercare
            if not steps:
                continue

            # Se adauga cuvantul final in set
            final_distinct_words.add(steps[-1])

        # Printeaza cuvintele finale
        print(
            f"\nCuvintele generate de gramatica sunt {len(final_distinct_words)}: {final_distinct_words}"
        )


def run_exercise_2_solution():
    path_maker = PathMaker(__file__, "data", "afd")
    file_path = path_maker.get_independent_OS_path("1.txt")

    # Initializam un obiect AFD gol.
    afd = AFD()

    try:
        # Incercam sa citim definitia AFD-ului din fisier.
        afd.citire(file_path)
    except Exception as e:
        # Daca apare o eroare la citire (format gresit, fisier lipsa, etc.),
        # o afisam si oprim executia functiei.
        print(e)
        return
    
    # Daca AFD-ul citit este valid conform regulilor de validare...
    if afd.validare():
        # ... il afisam (stari, alfabet, stare initiala, stari finale, tranzitii).
        afd.afisare()

        # Cerem utilizatorului un cuvant pentru verificare.
        cuvant = input("\nIntroduce-ti un cuvant pentru verificare: ")

        # Cat timp utilizatorul introduce un cuvant nenul (string nevid)...
        while cuvant:
            # Verificam cuvantul in AFD (acceptat / neacceptat / blocaj).
            afd.verificare(cuvant)

            # Cerem un nou cuvant; daca se apasa doar Enter, bucla se opreste.
            cuvant = input("\nIntroduce-ti un cuvant pentru verificare: ")
            
            
def run_exercise_3_solution():
    path_maker = PathMaker(__file__, "data", "afn")
    file_path = path_maker.get_independent_OS_path("1.txt")
    
    afn = AFN()
    
    try:
        afn.citire(file_path)
    except Exception as e:
        print(e)
        return
    
    if afn.validare():
        afn.afisare()

def main() -> None:
    # run_exercise_1_solution()
    # run_exercise_2_solution()
    run_exercise_3_solution()


if __name__ == "__main__":
    main()
