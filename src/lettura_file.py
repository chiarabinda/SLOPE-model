import pandas as pd
import os
import numpy as np

def lettura(path : str,
            sep : str = "\t", 
            colonne : tuple = ("n","u")
            ) -> pd.DataFrame:
    """
    Genera un dataframe a partire dalla lettura di un file txt avente due colonne.

    Parametri
    ----------
    path : str
        Percorso del file. 
    sep : str, default=tab
        Separatore campi. 
    colonne : tuple, default=("n","u")
        Tupla che contiene i nomi da assegnare alle colonne.

    Return
    ------
    df : DataFrame 
        Dataframe contenente due colonne, la prima corrispondente alla quota n (m) e la seconda corrispondente alla velocità u (m/s).

    Raises
    ------
    FileNotFoundError
        Se il file non viene trovato oppure il percorso inserito è errato.

    ValueError
        Se il file letto è vuoto.
        Se il file letto contiene dei NaN.
        Se il file letto ha più di due colonne.
        Se il file letto contiene dei numeri negativi.
        Se il file letto ha le colonne invertite. Possibile
        ricavarlo tramite la condizione: seconda colonna deve 
        essere u (valori < 6): se ci sono valori > 6, è n
    """
   
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Il file '{path}' non esiste o il percorso è sbagliato.")
    
    if os.path.getsize(path) == 0:
        raise ValueError(f"Il file '{path}' è vuoto.")
    
    df = pd.read_csv(path, sep=sep, dtype=float, header=None)
    
    if df.isna().any():
        raise ValueError(f"Il file '{path}' contiene valori mancanti (NaN).")
    
    if df.shape[1] != 2:
        raise ValueError(
            f"Il file '{path}' ha {df.shape[1]} colonne, ne sono ammesse al massimo 2."
        )
    
    if (df < 0).any(axis=None):
        raise ValueError(f"Il file '{path}' contiene valori negativi.")

    if (df.iloc[:, 1] > 6).any():
        raise ValueError(
            f"Il file '{path}': la seconda colonna contiene valori > 6, "
            "le colonne n e u sembrano invertite."
        )
    
    df.columns = list(colonne)
    return df

def delta_n(df : pd.DataFrame):
    """
    Calcola il valore di delta (m), lunghezza di scala corrispondente allo spessore dello strato in cui si sviluppa il vento di pendio, a partire dal valore di n per cui u = u_max.

    Parametri
    ----------
    df : DataFrame
        DataFrame contenente due colonne, la prima corrispondente alla quota n e la seconda alla velocità u.
    
    Return
    ------
    delta : float 
        Lunghezza di scala corrispondente allo spessore dello strato in cui si sviluppa il vento di pendio (m).
    """    

    n_u_max = df.iloc[df.iloc[:, 1].argmax(), 0] #valore di n che massimizza u
    delta = 4 * n_u_max / np.pi

    return delta

def thetas(df : pd.DataFrame,
           theta_0 : float,
           gamma : float,
           pr : float
           ):
    """
    Calcola il valore dell'anomalia di temperatura sulla superficie del pendio, theta_s (K), a partire dal valore u = u_max della seconda colonna del dataframe.

    Parametri
    ----------
    df : DataFrame
        DataFrame contenente due colonne, la prima corrispondente alla quota n e la seconda alla velocità u.
    theta_0 : float
        Temperatura potenziale di riferimento (K).
    gamma : float
        Gradiente verticale di temperatura potenziale (K/m).
    pr : float
        Numero di Prandtl.            
    
    Return
    ------
    theta_s : float 
        Misura dell'anomalia di temperatura sulla superficie del pendio, dove n = 0 (K).
    """    
    u_max = df.iloc[:, 1].max()
    theta_s = u_max * np.sqrt(2) * np.exp(np.pi / 4) * np.sqrt(theta_0 * gamma * pr / 9.81)

    return theta_s