import numpy as np
import matplotlib.pyplot as plt
from .u_prandtl import u_prandtl_teor, u_pr, delta_prandtl

def plot_profilo(n : np.ndarray,
                 u : np.ndarray,
                 par : tuple,
                 theta_s : float,
                 delta : float,
                 alpha : float,
                 theta_0 : float,
                 pr : float,
                 gamma : float,
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
        Parametri del fit : par[0] = theta_s (K), par[1] = ni (m^2/s).
    theta_s : float
        Misura dell'anomalia di temperatura sulla superficie del pendio, dove n = 0 (K).
    delta : float
        Lunghezza di scala corrispondente allo spessore dello strato in cui si sviluppa il vento di pendio (m).  
    alpha : float
        Angolo di inclinazione del pendio (°).
    theta_0 : float
        Temperatura potenziale di riferimento (K).
    pr : float
        Numero di Prandtl.
    gamma : float
        Gradiente verticale di temperatura potenziale (K/m).
    titolo : str
        Titolo del grafico.
    filename : str, optional
        Nome del file in cui salvare la figura (None per non salvare).

    """
    n_ax = np.linspace(0,130,261)
    
    delta_fit = delta_prandtl(alpha, theta_0, par[1], pr, gamma)
    u_fit = u_pr(n_ax, par[0], theta_0, pr, gamma, delta_fit)
    u_teor = u_prandtl_teor(n_ax, theta_s, pr, theta_0, gamma, delta)

    fig, ax = plt.subplots()
    ax.plot(u_fit, n_ax, label="fit")
    ax.plot(u, n, label="dati osservati")
    ax.plot(u_teor, n_ax, label="modello")

    ax.legend()
    ax.set_xlabel("u [m/s]")
    ax.set_ylabel("n [m]")
    ax.set_title(titolo)

    if filename is not None:
        fig.savefig(filename, bbox_inches="tight", dpi=300)
    return fig

def plot_sens_slope(n: np.ndarray,
                    par: np.ndarray,
                    alpha: float,
                    theta_0: float,
                    pr: float,
                    gamma: float,
                    alphas: tuple = (5, 10, 30, 45, 60, 75, 90),
                    filename: str = None
                    ) -> plt.Figure:
    """
    Sensibilità del profilo di velocità rispetto all'inclinazione del pendio, con theta_s e ni ottenuti dal fit.

    Parameters
    ----------
    n : np.ndarray
        Quota a cui vengono effettuate le misure di u (m), array 1D di lunghezza N.
    par : np.ndarray
        Parametri del fit: par[0] = theta_s (K), par[1] = ni (m^2/s).
    alpha : float
        Angolo del caso studio (°), evidenziato nel grafico.
    theta_0 : float
        Temperatura potenziale di riferimento (K).
    pr : float
        Numero di Prandtl.
    gamma : float
        Gradiente verticale di temperatura potenziale (K/m).
    alphas : tuple
        Angoli da confrontare (°). Quello del caso studio viene aggiunto automaticamente.
    filename : str
        Percorso del file di output.
    """
    theta_s, ni = par
    angoli = sorted(set(alphas) | {alpha})

    fig, ax = plt.subplots()
    for angle in angoli:
        delta = delta_prandtl(angle, theta_0, ni, pr, gamma)
        u_teo = u_pr(n, theta_s, theta_0, pr, gamma, delta)
        lw = 2.5 if angle == alpha else 1.2
        ax.plot(u_teo, n, lw=lw,
                 label=rf"{angle:g}$^\circ$, $\delta$ = {delta:.1f} m")

    ax.legend(fontsize="small")
    ax.set_xlabel("u [m/s]")
    ax.set_ylabel("n [m]")
    
    if filename is not None:
        fig.savefig(filename, bbox_inches="tight", dpi=300)
    return fig