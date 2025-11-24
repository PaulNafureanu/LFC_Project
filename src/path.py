from pathlib import Path
from typing import Union

PathLike = Union[Path, str]


class PathMaker:
    """
    Clasa pentru a construi cai de fisiere intr-un mod independent de sistemul de operare.

    Ideea este sa fixezi o „radacina” (entrypoint, de obicei fisierul main.py) si, optional, niste subfoldere de baza.
    Apoi sa generezi cai catre resurse specifice (fisiere) aflate dedesubtul subfolderelor de baza.
    """

    def __init__(self, root_file: PathLike, *base_parts: str) -> None:
        """
        Parameters
        ----------
        root_file:
            De obicei `__file__` din fisierul care reprezinta „radacina” proiectului (ex: main.py).
            Din acest fisier se deduce directorul de lucru.

        base_parts:
            Zero sau mai multe segmente de cale (foldere) care sunt comune pentru toate resursele pe care vrei sa le accesezi.

        Exemplu:

            Structura:

                .
                ├── data
                │   └── gramatica
                │       └── 1.txt
                ├── main.py
                └── src
                    └── path.py

            Din main.py:

                path_maker = PathMaker(__file__, "data", "gramatica")

            In acest caz:
            - root_dir   -> folderul in care se afla main.py
            - base_parts -> ("data", "gramatica")
        """
        # Directorul de baza (unde se află fisierul root_file, de ex. main.py)
        self.root_dir = Path(root_file).resolve().parent
        # Segmente de cale comune (ex: ("data", "gramatica"))
        self.base_parts = base_parts

    def get_independent_OS_path(self, *parts: str) -> Path:
        """
        Construiste si returneaza calea completa:

            root_dir / base_parts... / parts...

        Parameters
        ----------
        parts:
            Segmente de cale suplimentare (de ex. numele fisierului).

        Exemplu de utilizare din main.py:

            path_maker = PathMaker(__file__, "data", "gramatica")
            file_path = path_maker.get_independent_OS_path("1.txt")

        In functie de sistemul de operare, file_path ar putea fi:

        - pe Linux:   /home/Paul/Uni/LF/data/gramatica/1.txt
        - pe Windows: C:\\Users\\Paul\\Uni\\LF\\data\\gramatica\\1.txt
        - pe macOS:   /Users/Paul/Uni/LF/data/gramatica/1.txt
        """
        return self.root_dir.joinpath(*self.base_parts, *parts)
