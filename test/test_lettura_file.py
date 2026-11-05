import pytest
import numpy as np
from pathlib import Path
from src import lettura, delta_n

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

def test_massimo_a_n_zero():
    """
    Verifica che se il massimo di u cade a n = 0, delta = 0 non ha senso fisico.
    """
    n = np.array([0.0, 1.0, 2.0, 3.0])
    u = np.array([5.0, 3.0, 2.0, 1.0])  # massimo a n = 0
 
    with pytest.raises(ValueError):
        delta_n(n, u)

def test_massimo_a_n_negativo():
    """
    Verifica che se il massimo di u cade a quote negative (n_u_max < 0) venga generato un errore, come n = 0.
    """
    n = np.array([-2.0, -1.0, 0.5, 1.0])
    u = np.array([2.0, 4.0, 1.0, 0.5])  # massimo a n = -1
 
    with pytest.raises(ValueError):
        delta_n(n, u)        

def test_caso_valido():
    """
    Verifica che il valore di n pari al massimo di u restituisca una valore di delta = 4 * n_u_max/ pi corretto.
    """
    n = np.array([0.5, 1.0, 2.0, 3.0, 4.0])
    u = np.array([1.0, 2.5, 4.0, 3.0, 1.5])  # massimo a n = 2
    risultato = delta_n(n, u)
 
    assert risultato == pytest.approx(4 * 2.0 / np.pi)        