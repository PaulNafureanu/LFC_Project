from typing import List, Dict, Tuple, Set, Optional

Stare = str
Simbol = str

class Tranzitie:
    membrul_stang:Stare
    simbol:Simbol
    membrul_drept:Stare
    
    def __str__(self) -> str:
        # Afișare prietenoasă a tranziției, sub forma δ(q, a) = q'
        return f"δ({self.membrul_stang}, {self.simbol}) = {self.membrul_drept}"



class AFN:
    def __init__(self) -> None:
        self.Stari: List[str] = list()
        
        self.Sigma: List[str] = list()
        
        self.Delta:Dict[Tuple[Stare, Simbol], Set[Simbol]] = {}
        
        self.Reguli: List[Tranzitie] = list()
        
        self.StareInitiala: Optional[Stare] = None
        
        self.StariFinale: List[str] = list()
        
    def adauga_tranzitie(self, q:Stare, a:Simbol, p:Stare):
        if q not in self.Stari or p not in self.Stari:
            raise ValueError("Starile trebuie sa existe in Q pentru a adauga o tranzitie.")
        if a not in self.Sigma:
            raise ValueError("Starea trebuie sa fie in alfabetul Sigma pentru a adauga o tranzitie.")