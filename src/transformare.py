from typing import Set, List
from src.afn import AFN
from src.afd import AFD

class Transformator:
    def __init__(self, afn:AFN, afd:AFD) -> None:
        self.afn = afn
        self.afd = afd
        
    def transformare_AFN_in_AFD(self) -> None:
        if self.afn.StareInitiala:
            stare_initiala:Set[str] = set(self.afn.StareInitiala)        
            stari_finale:Set[Set[str]] = set()
            stari_finale.add(stare_initiala)
            
            for stare_finala in stari_finale:
                for simbol_afn in self.afn.Sigma:
                    stare_noua_finala:List[str] = list()
                    for stare_afn in stare_finala:
                        stare = self.afn.Delta[(stare_afn, simbol_afn)]
                        stare_noua_finala.extend(stare)
                    stari_finale.add(set(stare_noua_finala))