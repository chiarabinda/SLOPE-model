import numpy as np
import matplotlib.pyplot as plt

def plot_profilo(n : np.ndarray,
                 u : np.ndarray,
                 par : tuple,
                 u_pr : callable,
                 u_prandtl_teor : callable,
                 theta_s : float,
                 delta : float,
                 titolo : str,
                 filename: str = None
                ) -> plt.Figure:
    """
    Grafico dei profili di velocità u(n) dei dati reali, del fit e del modello teorico.
 
    Parameters
    ----------
    n : numpy.ndarray
        Quota a cui vengono effettuate le misure di u (m), array 1D di lunghezza N.
    u : numpy.ndarray
        Velocità del vento (m/s), array 1D di lunghezza N.
    par : float
        Parametri ottimali del fit, es. theta_s e ni.
    u_pr : callable
        Funzione che genera il profilo di velocità di cui fare il fit.
    u_prandtl_teor : callable
        Funzione che genera il profilo di velocità basato sul modello teorico.
    theta_s : float
        Misura dell'anomalia di temperatura sulla superficie del pendio, dove n = 0 (K).
    delta : float
        Lunghezza di scala corrispondente allo spessore dello strato in cui si sviluppa il vento di pendio (m).  
    titolo : str
        Titolo del grafico.
    filename : str, optional
        Nome del file in cui salvare la figura (None per non salvare).

    """
    n_ax = np.linspace(0,130,261)
    u_fit = u_pr(n_ax, par[0], par[1])
    u_teor = u_prandtl_teor(n_ax, theta_s, delta)

    fig, ax = plt.subplots()
    ax.plot(u_fit, n_ax, label="fit")
    ax.plot(u, n, label="real")
    ax.plot(u_teor, n_ax, label="model")

    ax.legend()
    ax.set_xlabel("u [m/s]")
    ax.set_ylabel("n [m]")
    ax.set_title(titolo)

    if filename is not None:
        fig.savefig(filename, bbox_inches="tight", dpi=300)
    return fig