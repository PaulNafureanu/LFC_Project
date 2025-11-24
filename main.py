from src.gramatica import Gramatica
from pathlib import Path


def get_independent_OS_path(*parts: str) -> Path:
    """
    Primeste un numar arbitrar de siruri de caractere reprezentand numele unor foldere si fisiere.
    Returneaza calea catre acea resursa, independent de sistemul de operare utilizat.

    Exemplu de utilizare pe urmatoarea structura a proiectului:

    .
    ├── data
    │   └── gramatica
    │       └── 1.txt
    ├── main.py

    Vrem calea (path-ul) pentru fisierul "1.txt" din folderul "gramatica", aflat în folderul "data".
    Folderul "data" este la acelasi nivel cu fisierul de intrare main.py al proiectului.

    Prin urmare, utilizam:

        file_path = get_independent_OS_path("data", "gramatica", "1.txt")

    Exemple de valori posibile pentru file_path (in functie de sistemul de operare):

    - pe Linux:   /home/Paul/Uni/LF/data/gramatica/1.txt
    - pe Windows: C:\\Users\\Paul\\Uni\\LF\\data\\gramatica\\1.txt
    - pe macOS:   /Users/Paul/Uni/LF/data/gramatica/1.txt
    """

    # Preia calea folderului in care fisierul curent (de ex. main.py) este stocat.
    # Exemplu pe Linux: daca main.py se afla in /home/Paul/Uni/LF,
    # atunci root_dir va fi Path("/home/Paul/Uni/LF").
    root_dir = Path(__file__).resolve().parent

    # Combina calea independent de OS, unind sub-partile primite în *parts.
    return root_dir.joinpath(*parts)


def main() -> None:

    # G1 = Gramatica()

    file_path_1 = get_independent_OS_path("data", "gramatica", "1.txt")

    print(file_path_1)

    # G1.citire(file_path_1)

    # G1.verificare()

    # G1.generare()

    # G1.afisare()


if __name__ == "__main__":
    main()
