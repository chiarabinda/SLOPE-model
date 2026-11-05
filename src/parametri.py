import numpy as np
from dataclasses import dataclass

PR_MIN_ARIA = 0.65
PR_MAX_ARIA = 0.80

@dataclass
class costanti_classe:
    """
    Classe contentente parametri fisici costanti in un fluido. 
    Il numero di Prandtl esprime il rapporto tra la viscosità cinematica e la diffusività termica di un fluido.

    Parameters
    ----------
    pr : float
        Numero di Prandtl.
    ni : float
        Viscosità cinematica molecolare.
    k :float
        Diffusività termica.
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
    Classe contenente parametri fisici del fluido aria, costanti in quest'ultima.

    Parameters
    ----------
    pr : float, default = 0.7
        Numero di Prandtl dell'aria.
    ni : float, default = 1.5e-5
        Viscosità cinematica molecolare dell'aria (m^2/s), assunta laminare.
    k :float, default= 2.2e-5
        Diffusività termica molecolare dell'aria (m^2/s), assunta laminare.
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
        
@dataclass
class termini_variabili:
    """
    Classe che contiene parametri di sistema specifici del caso studio cosiderato.

    Parameters
    ----------
    alpha : float
        Angolo di inclinazione della slope (°).
    gamma : float
        Gradiente verticale di temperatura potenziale (K/m).
    theta_0 :float
        Temperatura potenziale di riferimento (K).
    """        
    alpha : float
    gamma : float
    theta_0 : float

    def __post_init__(self):
        """
        Verifica che i valori siano decimali e positivi.
        """
        if not isinstance(self.alpha,float):
            raise TypeError(f"L'angolo di inclinazione deve essere decimale, ricevuto {type(self.alpha).__name__}")
        
        if not isinstance(self.gamma,float):
            raise TypeError(f"Il gradiente verticale di temperatura potenziale deve essere decimale, ricevuto {type(self.gamma).__name__}")
        
        if not isinstance(self.theta_0,float):
            raise TypeError(f"La temperatura potenziale deve essere decimale, ricevuto {type(self.theta_0).__name__}")

        if not (0 < self.alpha < 90):
            raise ValueError(f"L'angolo di inclinazione del pendio deve positivo e essere minore di 90°, ricevuto: {self.alpha}°)")
        
        if self.gamma <= 0:
            raise ValueError(f"Il gradiente verticale di temperatura potenziale deve essere positivo (> 0).")
        
        if self.theta_0 <= 0:
            raise ValueError(f"La temperatura potenziale deve essere positiva (> 0).")