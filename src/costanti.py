import numpy as np
from dataclasses import dataclass

PR_MIN_ARIA = 0.65
PR_MAX_ARIA = 0.80

@dataclass
class costanti_classe:
    """
    Classe contentente valori costanti. 

    Parametri
    ----------
    pr : float
        Numero di Prandtl
    ni : float
        Viscosità cinematica molecolare
    k :float
        Diffusività termica
    """
    pr : float 
    ni : float 
    k : float

    def __post_init__(self):
        """
        Verifica che i valori siano decimali e positivi.
        """
        if not isinstance(self.pr,float):
            raise TypeError(f"Il numero di Prandtl deve essere decimale, ricevuto {type(self.pr).__name__}")
        
        if not isinstance(self.ni,float):
            raise TypeError(f"La viscosità cinematica deve essere decimale, ricevuto {type(self.ni).__name__}")
        
        if not isinstance(self.k,float):
            raise TypeError(f"La diffusività termica deve essere decimale, ricevuto {type(self.k).__name__}")

        if self.pr <= 0:
            raise ValueError(f"Il numero di Prandtl deve essere positivo (> 0).")
        
        if self.ni <= 0:
            raise ValueError(f"La viscosità cinematica deve essere positiva (> 0).")
        
        if self.k <= 0:
            raise ValueError(f"La diffusività termica deve essere positiva (> 0).")

@dataclass        
class CostantiAria(costanti_classe):
    """
    Classe contenente valori costanti in aria.

    Parametri
    ----------
    pr : float, default = 0.7
        Numero di Prandtl dell'aria
    ni : float, default = 1.5e-5
        Viscosità cinematica molecolare dell'aria, assunta laminare
    k :float, default= 2.2e-5
        Diffusività termica molecolare dell'aria, assunta laminare
    """
    pr : float = 0.7 
    ni : float = 1.5e-5 
    k : float = 2.2e-5

    def __post_init__(self):
        """
        Verifica che il numero di Prandtl sia all'interno dell'intervallo tipico dell'aria.
        """
        super().__post_init__()
        if not (PR_MIN_ARIA <= self.pr <= PR_MAX_ARIA):
           raise ValueError(f"Il numero di Prandtl={self.pr} è fuori dall'intervallo tipico per l'aria")