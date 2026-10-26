import pandas as pd
import os

def lettura_file(path, sep="\t", colonne=("n","u")):
    """
    Lettura del file.

    Parametri
    ----------
    path : str
        Percorso del file. 
    sep : str, default=tab
        Separatore campi. 
    colonne : str, default=("n","u")
        Nomi da assegnare alle colonne.

    Raises
    ------
    FileNotFoundError
        Se il file non viene trovato oppure il percorso inserito è errato

    ValueError
        Se il file letto è vuoto.
        Se il file letto contiene dei NaN.
        Se il file letto ha più di due colonne.
        Se il file letto contiene dei numeri negativi.
        Se il file letto ha le colonne invertite. Possibile
        ricavarlo tramite la condizione: seconda colonna deve 
        essere u (valori < 6): se ci sono valori > 6, è n
    """
   
    df = pd.read_csv(path, sep=sep, header=None)

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Il file '{path}' non esiste o il percorso è sbagliato.")
    
    if os.path.getsize(path) == 0:
        raise ValueError(f"Il file '{path}' è vuoto.")
    
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