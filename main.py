from src.gramatica import Gramatica
from src.path import PathMaker


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

        print("\nTransformarile pas cu pas sunt:")
        G1.generare()


def main() -> None:
    run_exercise_1_solution()


if __name__ == "__main__":
    main()
