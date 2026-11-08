import numpy as np

def u_prandtl_teor(n : np.ndarray, 
                   theta_s : float, 
                   pr : float, 
                   theta_0 : float, 
                   gamma : float, 
                   delta : float
                   ) -> np.ndarray:
    """
    Calcola il profilo teorico di velocità in funzione dei valori di quota n utilizzando i parametri di sistema.

    Parameters
    ----------
    n : np.ndarray
        Array 1D corrispondente alla quota (m).
    theta_s : float 
        Misura dell'anomalia di temperatura sulla superficie del pendio (K).
    pr : float
        Numero di Prandtl. 
    theta_0 : float
        Temperatura potenziale di riferimento (K).
    gamma : float
        Gradiente verticale di temperatura potenziale (K/m).
    delta : float
        Lunghezza di scala corrispondente allo spessore dello strato in cui si sviluppa il vento di pendio (m).    
               
    Returns
    -------
    u_teo :  np.ndarray
        Profilo teorico di velocità del vento di pendio (m/s), array 1D della stessa lunghezza di n.    
    """    

    C = -theta_s * ( ( pr ** (-1) * 9.81 ) / (theta_0 * gamma) ) ** 0.5
    u_teo = C * np.exp(-n/delta) * np.sin(n/delta)

    return u_teo

def u_pr(n : np.ndarray,
         theta_s : float,
         theta_0 : float,
         pr : float,
         gamma : float,
         delta_pr : float
         ) -> np.ndarray:
    """
    Calcola il profilo di velocità, del modello di cui fare il fit, in funzione dei 
    valori di quota n e usando i parametri di sistema.
    
    Parameters
    ----------
    n : np.ndarray
        Array 1D corrispondente alla quota (m).
    theta_s : float 
        Misura dell'anomalia di temperatura sulla superficie del pendio (K).
    theta_0 : float
        Temperatura potenziale di riferimento (K).    
    pr : float
        Numero di Prandtl. 
    gamma : float
        Gradiente verticale di temperatura potenziale (K/m).    
    delta_pr : float
        Lunghezza di scala corrispondente allo spessore dello strato in cui si sviluppa il vento di pendio (m).    
               
    Returns
    -------
    u_for_fit :  np.ndarray
        Profilo di velocità del vento di pendio da fittare con il modello (m/s), array 1D della stessa lunghezza di n.    
    """

    u_for_fit = -theta_s * (  pr**(-1) * (9.81 )/(theta_0*gamma) )**0.5 * np.exp(-n/delta_pr) * np.sin(n/delta_pr)

    return u_for_fit

def delta_prandtl(alpha : float,
                  theta_0 : float,
                  ni : float,
                  pr : float,
                  gamma : float
                  ) -> float:
    """
    Calcola lo spessore di aria (m) al di sopra del pendio in cui si sviluppa il vento (upslope o downslope).
    
    Parameters
    ----------
    alpha : float
        Angolo di inclinazione del pendio (°).
    theta_0 : float
        Temperatura potenziale di riferimento (K). 
    ni : float
        Viscosità cinematica molecolare (m^2/s).       
    pr : float
        Numero di Prandtl. 
    gamma : float
        Gradiente verticale di temperatura potenziale (K/m).   
            
    Returns
    -------
    delta_pr : float 
        Lunghezza di scala corrispondente allo spessore di aria in cui si sviluppa il vento di pendio (m).        
    """

    alpha_rad = np.deg2rad(alpha)
    delta_pr = ( (4*theta_0*ni**2*pr**(-1)) / (9.81*gamma*(np.sin(alpha_rad))**2) )**0.25
    
    return delta_pr