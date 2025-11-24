from src.gramatica import Gramatica
from src.path import PathMaker


def run_exercise_1_solution():
    path_maker = PathMaker(__file__, "data", "gramatica")

    # Se poate incerca si cu "2.txt" si "3.txt"
    file_path = path_maker.get_independent_OS_path("1.txt")

    G1 = Gramatica()
    G1.citire(file_path)
    G1.afisare()

    # G1.verificare()

    # G1.generare()


def main() -> None:
    run_exercise_1_solution()


if __name__ == "__main__":
    main()
