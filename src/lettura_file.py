import pandas as pd
import os
import numpy as np

U_M = 6  # valore massimo plausibile di u (m/s)

def lettura(path : str,
            sep : str = "\t",
            ) -> tuple[np.ndarray, np.ndarray]:
    """
    Genera due array 1D, corrispondenti a n ed u, a partire dalla lettura di un file txt avente due colonne.

    Parameters
    ----------
    path : str
        Percorso del file. 
    sep : str, default=tab
        Separatore campi. 

    Returns
    -------
    n : numpy.ndarray
        Quota a cui vengono effettuate le misure di u (m), array 1D di lunghezza N.
    u : numpy.ndarray
        Velocità del vento (m/s), array 1D di lunghezza N.

    Raises
    ------
    FileNotFoundError
        Se il file non viene trovato oppure il percorso inserito è errato.

    ValueError
        Se il file letto è vuoto.
        Se il file letto contiene dei NaN.
        Se il file letto ha più di due colonne.
        Se il file letto contiene dei numeri negativi.
        Se il file letto ha le colonne invertite. Possibile ricavarlo tramite la condizione per cui la seconda colonna deve essere u < 6: se ci sono valori > 6, è n.
    """
   
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Il file '{path}' non esiste o il percorso è sbagliato.")
    
    if os.path.getsize(path) == 0:
        raise ValueError(f"Il file '{path}' è vuoto.")
    
    dati = pd.read_csv(path, sep=sep, dtype=float, header=None)
    
    if dati.isna().any(axis=None):
        raise ValueError(f"Il file '{path}' contiene valori mancanti (NaN).")
    
    if dati.shape[1] != 2:
        raise ValueError(
            f"Il file '{path}' ha {dati.shape[1]} colonne, ne sono ammesse 2."
        )
    
    if (dati < 0).any(axis=None):
        raise ValueError(f"Il file '{path}' contiene valori negativi.")

    if (dati.iloc[:, 1] > U_M).any():
        raise ValueError(
            f"Il file '{path}': la seconda colonna contiene valori > {U_M}, le colonne n e u sembrano invertite."
        )
    
    n, u = dati.to_numpy().T
    return n, u

def delta_n(n: np.ndarray,
            u : np.ndarray
            ) -> float:
    """
    Calcola il valore di delta (m), lunghezza di scala corrispondente allo spessore dello strato in cui si sviluppa il vento di pendio, a partire dal valore di n per cui u = u_max. Viene utilizzato il modello di Prandtl

    Parameters
    ----------
    n : numpy.ndarray
        Quota a cui vengono effettuate le misure di u (m), array 1D di lunghezza N.
    u : numpy.ndarray
        Velocità del vento (m/s), array 1D di lunghezza N.
    
    Returns
    -------
    delta : float 
        Lunghezza di scala corrispondente allo spessore dello strato in cui si sviluppa il vento di pendio (m).

    Raises
    ------
    ValueError
        Se il valore massimo di velocità u si ha per quote n minori o uguali a 0.    
    """    

    n_u_max = n[u.argmax()] #valore di n che massimizza u

    if n_u_max <= 0:
        raise ValueError(
        f"Il massimo di u cade a n = {n_u_max} m: delta = 0 non ha significato fisico, controllare i dati.")

    delta = 4 * n_u_max / np.pi
    
    return delta

def thetas(u : np.ndarray,
           theta_0 : float,
           gamma : float,
           pr : float
           ) -> float:
    """
    Calcola il valore dell'anomalia di temperatura sulla superficie del pendio, theta_s (K), a partire dal valore u = u_max. Deriva dalle formule del modello di Prandtl.

    Parameters
    ----------
    u : numpy.ndarray
        Velocità del vento (m/s), array 1D di lunghezza N.
    theta_0 : float
        Temperatura potenziale di riferimento (K).
    gamma : float
        Gradiente verticale di temperatura potenziale (K/m).
    pr : float
        Numero di Prandtl.            
    
    Returns
    -------
    theta_s : float 
        Misura dell'anomalia di temperatura sulla superficie del pendio, dove n = 0 (K).
    """    
    u_max = u.max()
    theta_s = u_max * np.sqrt(2) * np.exp(np.pi / 4) * np.sqrt(theta_0 * gamma * pr / 9.81)

    return theta_s