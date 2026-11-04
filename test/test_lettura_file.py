import pytest
import numpy as np
from pathlib import Path
from src import lettura

DATA_DIR = Path(__file__).parent / "txt"

def test_lettura_file_vuoto():
    """
    Verifica che un file di testo vuoto generi un errore.
    """
    with pytest.raises(ValueError):
        lettura(DATA_DIR/"vuoto.txt")
   
def test_lettura_file_nan():
    """
    Verifica che un file di testo con valori mancanti 
    generi un errore.
    """
    with pytest.raises(ValueError):
        lettura(DATA_DIR/"NaN.txt")

def test_lettura_file_piùcolonne():
    """
    Verifica che un file di testo che contiene più di due 
    colonne generi un errore.
    """    
    with pytest.raises(ValueError):
        lettura(DATA_DIR/"3_colonne.txt")

def test_lettura_file_n_negativa():
    """
    Verifica che un file di testo contenete valori di n 
    negativi generi un errore.
    """
    with pytest.raises(ValueError):
        lettura(DATA_DIR/"n_negativa.txt")   

def test_lettura_file_u_negativa():
    """
    Verifica che un file di testo contenete valori di u 
    negativi generi un errore.
    """
    with pytest.raises(ValueError):
        lettura(DATA_DIR/"u_negativa.txt")

def test_lettura_file_colonne_invertite():
    """
    Verifica che un file di testo con le colonne invertite
    generi un errore.
    """    
    with pytest.raises(ValueError):
        lettura(DATA_DIR/"u_n.txt")