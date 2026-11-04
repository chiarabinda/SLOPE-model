import pytest
from src import costanti_classe, CostantiAria, PR_MIN_ARIA, PR_MAX_ARIA, termini_variabili

@pytest.mark.parametrize("pr, ni, k, expected_exception", [
    (1, 1.0, 1.0, TypeError),   # Numero intero per Prandtl, pr
    (1.0, 1, 1.0, TypeError),   # Numero intero per viscosità cinematica, ni
    (1.0, 1.0, 1, TypeError),   # Numero intero per diffusività termica, k
    (-1.0, 1.0, 1.0, ValueError),   # Numero di Prandtl negativo
    (1.0, -1.0, 1.0, ValueError),   # Viscosità cinematica negativa
    (1.0, 1.0, -1.0, ValueError),   # Diffusività termica negativa
])

def test_costanti(pr, ni, k, expected_exception):
    """
    Verifica che tipi errati o valori negativi, dei parametri fisici costanti in un fluido, generino un errore.
    """
    with pytest.raises(expected_exception):
        costanti_classe(pr=pr, ni=ni, k=k)

def test_CostantiAria():
    """
    Verifica i valori di default dei parametri fisici del fluido aria.
    """
    c = CostantiAria()
    assert c.pr == 0.7
    assert c.ni == 1.5e-5
    assert c.k == 2.2e-5

@pytest.mark.parametrize("pr", [PR_MIN_ARIA, 0.7, PR_MAX_ARIA])
def test_aria_pr_valido(pr):
    """
    Verifica che il numero di Prandtl dentro l'intervallo, estremi inclusi, sia accettato.
    """
    assert CostantiAria(pr=pr).pr == pr    

@pytest.mark.parametrize("pr", [7.0, 0.01, PR_MIN_ARIA - 0.01, PR_MAX_ARIA + 0.01])
def test_aria_pr_fuori_range(pr):
    """
    Verifica che il numero di Prandtl fuori dall'intervallo tipico per l'aria generi un errore.
    """
    with pytest.raises(ValueError, match="aria"):
        CostantiAria(pr=pr)    


@pytest.mark.parametrize("alpha, gamma, theta_0, expected_exception", [
    (20, 0.002, 200.0, TypeError),      # Numero intero per l'angolo di inclinazione, alpha
    (20.0, 1, 200.0, TypeError),        # Numero intero per il gradiente verticale di temperatura potenziale, gamma
    (20.0, 0.002, 200, TypeError),      # Numero intero per la temperatura potenziale, theta_0
    (0.0, 0.002, 200.0, ValueError),    # Angolo di inclinazione nullo
    (-10.0, 0.002, 200.0, ValueError),  # Angolo di inclinazione negativo
    (90.0, 0.002, 200.0, ValueError),   # Angolo di inclinazione pari a 90°
    (120.0, 0.002, 200.0, ValueError),  # Angolo di inclinazione maggiore di 90°
    (20.0, 0.0, 200.0, ValueError),     # Gradiente verticale nullo
    (20.0, -0.002, 200.0, ValueError),  # Gradiente verticale negativo
    (20.0, 0.002, 0.0, ValueError),     # Temperatura potenziale nulla
    (20.0, 0.002, -200.0, ValueError),  # Temperatura potenziale negativa
])
def test_termini_variabili(alpha, gamma, theta_0, expected_exception):
    """
    Verifica che tipi errati o valori fuori range, dei parametri di sistema specifici del caso studio, generino un errore.
    """
    with pytest.raises(expected_exception):
        termini_variabili(alpha=alpha, gamma=gamma, theta_0=theta_0)        