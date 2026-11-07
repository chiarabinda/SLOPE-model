import numpy as np
from src import u_prandtl_teor, u_pr

n = np.linspace(0, 500, 101)  # include n = 0
theta_s = 1.0
pr = 1.0
theta_0 = 300.0
gamma = 0.003
delta = 100.0
alpha=30.0
ni=1.5e-5

#profilo teorico per test uteo
u_teo = u_prandtl_teor(n, theta_s, pr, theta_0, gamma, delta)

#parametri per test delta
angle = np.deg2rad(alpha)
delta_test = ( (4*theta_0*ni**2*pr**(-1)) / (9.81*gamma*(np.sin(angle))**2) )**0.25

#profilo del modello di cui fare il fit per test ufit
u_fit = u_pr(n, theta_s, pr, theta_0, gamma, delta_test)

def test_uteo_no_nan_inf():
    """
    Verifica che il profilo teorico con numeri non finiti (NaN o inf) generi un errore.
    """ 
    assert np.isfinite(u_teo).all()

def test_uteo_tipo():
    """
    Genera un errore se i valori del profilo teorico di velocità non sono contenuti in un array.
    """ 
    assert isinstance(u_teo, np.ndarray)    

def test_uteo_stessa_forma_n():
    """
    Verifica che se il numero di valori che compongono l'array del profilo teorico è diverso dal numero di valori dell'array di n venga generato un errore.
    """
    assert u_teo.shape == n.shape

def test_uteo_0_per_n_0():
    """
    Genera un errore se i valori del profilo teorico di veocità non si annullano in n = 0, deve accadere perché sin(0) = 0.
    """
    assert np.allclose(u_teo[n == 0], 0.0)
     
def test_ufit_no_nan_inf():
    """
    Verifica che il profilo di cui fare il fit avente numeri non finiti (NaN o inf) generi un errore.
    """ 
    assert np.isfinite(u_fit).all()

def test_ufit_tipo():
    """
    Genera un errore se i valori del profilo di velocità da fittare non sono contenuti in un array.
    """ 
    assert isinstance(u_fit, np.ndarray)    

def test_ufit_stessa_forma_n():
    """
    Verifica che se il numero di valori che compongono l'array del profilo di cui fare il fit è diverso dal numero di valori dell'array di n venga generato un errore.
    """
    assert u_fit.shape == n.shape

def test_ufit_0_per_n_0():
    """
    Genera un errore se i valori del profilo di veocità da fittare non si annullano in n = 0, deve accadere perché sin(0) = 0.
    """
    assert np.allclose(u_fit[n == 0], 0.0)    

def test_delta_no_nan_inf():
    """
    Verifica che la lunghezza di scala con numeri non finiti (NaN o inf) e negativi generi un errore.
    """ 
    assert np.isfinite(delta_test).all()
    assert delta_test > 0  