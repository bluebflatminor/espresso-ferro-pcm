"""
Simulation 3: Write pulse electrostatic crosstalk at 3-5 µm cell pitch
FEniCS finite element simulation — Poisson + Landau-Khalatnikov dynamics

Computes fringe electric field from a TiN write pulse at adjacent cell
Al:HfO2 and evaluates partial switching probability vs pitch and voltage.

Research design: Nils Haaland (nhaaland@yahoo.com) — Solbakken Research Initiative
Code drafted with Claude (Anthropic)

Usage:
    python sim3_crosstalk.py                    # default: 3um pitch, 4V
    python sim3_crosstalk.py --pitch 5.0        # 5 µm pitch
    python sim3_crosstalk.py --voltage 3.0      # 3V write pulse
    python sim3_crosstalk.py --sweep            # full pitch/voltage sweep
    python sim3_crosstalk.py --no-fenics        # analytical only

Dependencies: fenics, mshr, numpy, matplotlib, scipy
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import epsilon_0

try:
    from fenics import *
    from mshr import Box, generate_mesh
    FENICS_AVAILABLE = True
except ImportError:
    FENICS_AVAILABLE = False
    print("WARNING: FEniCS not available. Using analytical approximation.")

# ─────────────────────────────────────────────────────────────────
# MATERIAL PARAMETERS
# ─────────────────────────────────────────────────────────────────

# Layer thicknesses (metres)
T_SIO2    = 10e-9
T_AL2O3   = 1e-9
T_HFO2    = 10e-9
T_TIN     = 10e-9
T_DIAMOND = 5e-6

# Stack z-coordinates (metres)
Z_AL2O3_BOT  = T_SIO2
Z_HFO2_BOT   = T_SIO2 + T_AL2O3
Z_HFO2_TOP   = T_SIO2 + T_AL2O3 + T_HFO2
Z_TIN_TOP    = Z_HFO2_TOP + T_TIN
STACK_HEIGHT = Z_TIN_TOP + T_DIAMOND

# Relative permittivities
EPS_SIO2    = 3.9
EPS_AL2O3   = 9.0
EPS_HFO2    = 25.0
EPS_DIAMOND = 5.7

# Ferroelectric parameters (Al:HfO2, Xu et al. 2025)
PR  = 15e-6    # C/m2 — remnant polarisation
EC  = 1.5e8    # V/m  — coercive field

# Write pulse
V_WRITE    = 4.0     # V
T_PULSE    = 10e-9   # s
T_RISE     = 1e-9    # s

# ─────────────────────────────────────────────────────────────────
# LANDAU-KHALATNIKOV MODEL
# ─────────────────────────────────────────────────────────────────

def lk_params(pr=PR, ec=EC):
    """Fit Landau coefficients to match Pr and Ec."""
    alpha = -3 * ec / (2 * pr)
    beta  = -alpha / (2 * pr**2)
    return alpha, beta


def simulate_switching(E_adjacent, dt=1e-11):
    """
    Simulate polarisation dynamics in adjacent cell under fringe field.
    Initial state: P = +Pr (programmed ON)
    Returns switching fraction and time series.
    """
    alpha, beta = lk_params()
    gamma_lk    = 1e-3   # viscosity (Pas)
    t_arr       = np.arange(0, T_PULSE, dt)

    def E_pulse(t):
        if t < T_RISE:
            return E_adjacent * t / T_RISE
        elif t < T_PULSE - T_RISE:
            return E_adjacent
        elif t < T_PULSE:
            return E_adjacent * (T_PULSE - t) / T_RISE
        return 0.0

    P = PR
    P_arr = [P]

    for i in range(1, len(t_arr)):
        E    = E_pulse(t_arr[i])
        dF   = 2*alpha*P + 4*beta*P**3
        dP   = (E - dF) / gamma_lk * dt
        P    = P + dP
        P_arr.append(P)

    P_arr = np.array(P_arr)
    switch_frac = (PR - P_arr[-1]) / (2 * PR)
    return switch_frac, t_arr, P_arr


# ─────────────────────────────────────────────────────────────────
# ANALYTICAL FRINGE FIELD
# ─────────────────────────────────────────────────────────────────

def fringe_field_analytical(pitch_m, v_write):
    """
    Order-of-magnitude fringe field estimate at adjacent cell.
    Use FEniCS for accurate results.
    """
    E_direct = v_write / (
        T_HFO2/EPS_HFO2 + T_AL2O3/EPS_AL2O3 + T_SIO2/EPS_SIO2
    )
    lateral   = pitch_m * 0.2
    decay     = np.exp(-np.pi * lateral / STACK_HEIGHT)
    return E_direct * (T_HFO2 / pitch_m) * decay


# ─────────────────────────────────────────────────────────────────
# FENICS SIMULATION
# ─────────────────────────────────────────────────────────────────

def run_fenics(pitch_m, v_write, resolution=40):
    """3D FEM electrostatics — returns E field at adjacent cell."""
    if not FENICS_AVAILABLE:
        return fringe_field_analytical(pitch_m, v_write)

    domain = Box(Point(0,0,0), Point(pitch_m, pitch_m, STACK_HEIGHT))
    mesh   = generate_mesh(domain, resolution)
    V      = FunctionSpace(mesh, 'CG', 2)

    eps = Expression(
        '''x[2] < z_al2o3 ? eps_sio2 :
           x[2] < z_hfo2_bot ? eps_al2o3 :
           x[2] < z_hfo2_top ? eps_hfo2 :
           x[2] < z_tin_top  ? 1e6 :
           eps_diamond''',
        degree=0,
        eps_sio2=EPS_SIO2, eps_al2o3=EPS_AL2O3,
        eps_hfo2=EPS_HFO2, eps_diamond=EPS_DIAMOND,
        z_al2o3=Z_AL2O3_BOT, z_hfo2_bot=Z_HFO2_BOT,
        z_hfo2_top=Z_HFO2_TOP, z_tin_top=Z_TIN_TOP
    )

    active = CompiledSubDomain(
        'near(x[2], zt, tol) && '
        'x[0]>=p*0.1 && x[0]<=p*0.9 && '
        'x[1]>=p*0.1​​​​​​​​​​​​​​​​
