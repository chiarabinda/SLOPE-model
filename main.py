import argparse
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

from src.lettura_file import lettura, delta_n, thetas
from src.parametri import CostantiAria, termini_variabili
from src.u_prandtl import u_pr, delta_prandtl
from src.plot import plot_profilo, plot_sens_slope

CARTELLA_OUTPUT_DEFAULT = Path(__file__).resolve().parent / "output"
TITOLO_DEFAULT = "Profilo di velocità del vento di pendio"
NOME_DEFAULT = "profilo_vento"


def parse_args() -> argparse.Namespace:
    """
    Legge gli argomenti da riga di comando.

    Returns
    -------
    argparse.Namespace
        Argomenti della riga di comando analizzati.
    """
    parser = argparse.ArgumentParser(
        description="Fit del profilo di velocità del vento di pendio con il modello di Prandtl."
    )
    parser.add_argument(
        "file", 
        help="Percorso del file txt con i dati (colonne: n, u)."
        )
    parser.add_argument(
        "--alpha", 
        type=float, 
        required=True,
        help="Angolo di inclinazione del pendio (°)."
        )
    parser.add_argument(
        "--gamma", 
        type=float, 
        required=True,
        help="Gradiente verticale di temperatura potenziale (K/m)."
        )
    parser.add_argument(
        "--theta0", 
        type=float, 
        required=True,
        help="Temperatura potenziale di riferimento (K)."
        )
    parser.add_argument(
        "--sep", 
        default="\\t",
        help="Separatore delle colonne nel file (default: tabulazione, '\\t')."
        )
    parser.add_argument(
        "--titolo", 
        default=TITOLO_DEFAULT,
        help=f"Titolo del plot (default: '{TITOLO_DEFAULT}')."
        )
    parser.add_argument(
        "--nome", 
        default=NOME_DEFAULT,
        help=f"Nome del file di output, con o senza estensione (default: '{NOME_DEFAULT}')."
        )
    parser.add_argument(
        "--output-dir", 
        type=Path, 
        default=CARTELLA_OUTPUT_DEFAULT,
        help="Cartella in cui salvare plot e file di testo (default: 'output' accanto a main)."
        )
    return parser.parse_args()


def main():
    """
    Punto di ingresso CLI: analizza gli argomenti ed esegue la simulazione.
    """

    args = parse_args()

    # Lettura file dati
    sep = "\t" if args.sep == "\\t" else args.sep
    try:
        n, u = lettura(args.file, sep=sep)
    except (FileNotFoundError, ValueError) as e:
        sys.exit(f"Errore: {e}")

    # Parametri: costanti dell'aria e parametri di sistema inseriti da riga di comando
    aria = CostantiAria()
    try:
        sistema = termini_variabili(alpha=args.alpha, gamma=args.gamma, theta_0=args.theta0)
    except (TypeError, ValueError) as e:
        sys.exit(f"Errore: {e}")
    pr, alpha, gamma, theta_0 = aria.pr, sistema.alpha, sistema.gamma, sistema.theta_0

    # Delta e theta_s ricavati dai dati
    try:
        delta_dati = delta_n(n, u)
    except ValueError as e:
        sys.exit(f"Errore: {e}")
    theta_s_dati = thetas(u, theta_0, gamma, pr)

    # Fit: parametri liberi theta_s e ni
    def modello(n_, theta_s, ni):
        delta = delta_prandtl(alpha, theta_0, ni, pr, gamma)
        return u_pr(n_, theta_s, theta_0, pr, gamma, delta)

    # nel modello u = -theta_s * ...; per avere u > 0, theta_s < 0
    p0 = [-theta_s_dati, 1.0]
    par, cov = curve_fit(
        modello, n, u, p0=p0, bounds=([-5, 1e-12], [5, np.inf]),
    )
    errori = np.sqrt(np.diag(cov))
    delta_model = delta_prandtl(alpha, theta_0, par[1], pr, gamma)

    # Cartella di output e nomi dei file (txt e plot condividono il nome)
    nome = args.nome
    if not nome.lower().endswith((".png", ".pdf", ".jpg", ".jpeg")):
        nome += ".png"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    percorso_plot = args.output_dir / nome
    percorso_txt = percorso_plot.with_suffix(".txt")

    righe = [
        "_________FIT__________",
        f"theta_s = {par[0]:.3f} ± {errori[0]:.3f} K",
        f"ni = {par[1]:.3f} ± {errori[1]:.3f} m^2/s",
        f"delta = {delta_model:.3f} m",
    ]
    with open(percorso_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(righe) + "\n")
    print(f"Risultati salvati in '{percorso_txt}'.")

    # Plot profili verticali (theta_s ha segno invertito così da avere u positivo)
    plot_profilo(n, u, par, -theta_s_dati, delta_dati,
                 alpha, theta_0, pr, gamma,
                 titolo=args.titolo,
                 filename=str(percorso_plot))
    print(f"Grafico salvato in '{percorso_plot}'.")

    # Plot sensibilità di u rispetto all'inclinazione della slope
    percorso_sens = args.output_dir / f"{percorso_plot.stem}_sens_slope.png"
    plot_sens_slope(n, par, alpha, theta_0, pr, gamma, filename=str(percorso_sens))
    print(f"Grafico di sensibilità salvato in '{percorso_sens}'.")


if __name__ == "__main__":
    main()
