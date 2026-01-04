from typing import Set, List, Dict, FrozenSet, Tuple, Optional
from src.afn import AFN

Stare = str
Simbol = str

class AFD:
    Stari: List[str] = list()
    Sigma: List[str] = list()
    Delta: Dict[Tuple[Stare, Simbol], Stare] = {}
    StareInitiala: Optional[str] = None
    StariFinale: List[str] = list()

class StariFinale:
    name_to_set: Dict[str, FrozenSet[str]] = {}
    set_to_name: Dict[FrozenSet[str], str] = {}
    names: List[str] = list()
    
    def add(self, name:str, s:Set[str]):
        fs = frozenset(s)
        self.name_to_set[name] = fs
        self.set_to_name[fs] = name
        self.names.append(name)
    
    def get_set(self, name:str) -> FrozenSet[str]:
        return self.name_to_set[name]

    def get_name(self, s:Set[str]) -> str:
        return self.set_to_name[frozenset(s)]


class Transformator:
    def __init__(self, afn:AFN) -> None:
        self.afn = afn
        
    def transformare_AFN_in_AFD(self) -> AFD:
        if self.afn.StareInitiala:
            stari_finale:StariFinale = StariFinale()
            stari_finale.add("S1", set(self.afn.StareInitiala))
            
            Sigma:List[str] = self.afn.Sigma
            Delta: Dict[Tuple[Stare, Simbol], Stare] = {}

            for name in stari_finale.names:
                for simbol in Sigma:
                    stare_noua:List[str] = list()
                    for stare_afn in stari_finale.get_set(name):
                        stare_noua.extend(set(self.afn.Delta[(stare_afn, simbol)]))
                    new_name = f"S{len(stari_finale.names) + 1}"
                    stari_finale.add(new_name, set(stare_noua))
                    Delta[(name, simbol)] = new_name
            
            final_names = stari_finale.names
            final_names.remove("S1")
            
            afd = AFD()
            afd.Stari = stari_finale.names
            afd.Sigma = Sigma
            afd.Delta = Delta
            afd.StareInitiala = "S1"
            afd.StariFinale = final_names
            return afd
        else:
            raise ValueError("Starea initiala in AFN trebuie sa existe")

            