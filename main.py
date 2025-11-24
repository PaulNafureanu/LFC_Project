from src.gramatica import Gramatica
from src.path import PathMaker


def main() -> None:

    # G1 = Gramatica()

    path_maker = PathMaker(__file__, "data", "gramatica")
    file_path_1 = path_maker.get_independent_OS_path("1.text")
    print(file_path_1)

    # G1.citire(file_path_1)

    # G1.verificare()

    # G1.generare()

    # G1.afisare()


if __name__ == "__main__":
    main()
