"""
Simulation 2 — Phase 2: Optical load retention model
Ferroelectric photonic memory — Pauli blocking threshold under 1550 nm flux

Feeds from Quantum ESPRESSO epsilon.x outputs.
Computes steady-state photocarrier density under continuous waveguide
illumination and evaluates whether the Pauli blocking threshold is crossed.

Research design: Nils Haaland (nhaaland@yahoo.com) — Solbakken Research Initiative
Code drafted with Claude (Anthropic)

Usage:
    python sim2_retention.py                    # default sweep
    python sim2_retention.py --power 1.0        # single power (mW/um2)
    python sim2_retention.py --tau_nr 1e-12     # single tau_nr (s)
    python sim2_retention.py --plot             # generate retention map

Dependencies: numpy, scipy, matplotlib
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar, c, epsilon_0

# ─────────────────────────────────────────────────────────────────
# PHYSICAL CONSTANTS AND ARCHITECTURE PARAMETERS
# ─────────────────────────────────────────────────────────────────

LAMBDA_NM   = 1550.0
OMEGA       = 2 * np.pi * c / (LAMBDA_NM * 1e-9)
H_OMEGA_EV  = 0.80

# Pauli blocking threshold
N_BLOCKING  = 1.18e13    # cm-2 — requires E_F = 0.40 eV

# Ferroelectric programmed states
N_FE_ON     = 1.5e13     # cm-2 — ON state (above threshold)
N_FE_OFF    = 5e12       # cm-2 — OFF state (below threshold)

# Optical conductivity from QE epsilon.x
# Replace placeholder values with your epsilon.x results
# Format: {n_carrier_cm2: sigma_sheet_S}
SIGMA_TABLE = {
    0:       6.08e-5,
    1e12:    5.50e-5,
    5e12:    4.20e-5,
    1e13:    2.10e-5,
    1.18e13: 0.50e-5,
    1.5e13:  0.10e-5,
}

# Waveguide geometry
MODE_OVERLAP = 0.02       # Gamma — from FDTD (range 0.01-0.03)
N_EFF        = 1.8        # effective mode index, 330nm SiN at 1550nm

# ─────────────────────────────────────────────────────────────────
# PHOTOCARRIER GENERATION MODEL
# ─────────────────────────────────────────────────────────────────

def absorption_coefficient(sigma_sheet, mode_overlap, n_eff):
    """Alpha (m-1) from graphene sheet conductance."""
    return sigma_sheet * mode_overlap / (epsilon_0 * c * n_eff)


def photocarrier_generation_rate(optical_power_W_per_m2, alpha_m):
    """G (cm-2 s-1) from optical intensity and absorption."""
    G​​​​​​​​​​​​​​​​
