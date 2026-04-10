# espresso-ferro-pcm

**Simulation specifications and runnable input stubs for three open computational problems in graphene-on-diamond ferroelectric photonic memory.**

*Research design and scientific direction: Nils Haaland (nhaaland@yahoo.com) — Solbakken Research Initiative (Independent)*
*Repository structure and code drafted with Claude (Anthropic)*
*Licence: MIT*

---

## What this is

This repository contains runnable input file stubs for three simulations that would materially advance open questions in the Diamond-Integrated FERRO-PCM photonic memory architecture — a non-volatile weight storage system for photonic AI accelerators built on single-crystal diamond (111), epitaxial graphene, and Al:HfO₂ ferroelectric gating.

None of these simulations appear to have been run for this specific material system. The stubs are written to be dropped into a working Quantum ESPRESSO, LAMMPS, or FEniCS environment with minimal modification.

This is not a collaboration proposal. It is an open invitation: if any of these problems overlap with your group's existing work, the architecture specification and full prior parameter files are available on request.

---

## Programme context

This repository is a companion to the four-paper Solbakken photonic memory programme:

| Paper | Title | Status |
|-------|-------|--------|
| Paper 1 | Ferroelectric Grain Boundary Polarization as a Hidden Variability Source in Photonic Memory Arrays | Complete |
| Paper 2 | The Weight Bottleneck: Why Reliable Non-Volatile Photonic Memory Is the Next Critical Barrier in Photonic AI Acceleration | Complete |
| Paper 3 | Diamond-Integrated FERRO-PCM Non-Volatile Photonic Weight Memory | Draft |
| Paper 4 | Graphene Integration Route Selection for Ferroelectric Photonic Memory: A Bayesian Quality Assessment Across Ten Process Scenarios | Complete — arXiv pending |

Paper 4 simulation code and prior parameter files:
**[graphene-photonic-memory-routes](https://github.com/nhaaland/graphene-photonic-memory-routes)**

---

## The three simulations

### Simulation 1 — Ni island formation and graphene nucleation on SCD(111)
**Tools:** Quantum ESPRESSO (pw.x, NEB) + LAMMPS (ReaxFF)
**Question:** Does Ni catalyst feature geometry at sub-50 nm scales govern graphene domain size and nucleation density on SCD(111)?
**Why it matters:** Route F has the highest quality ceiling of any route evaluated in Paper 4 but is currently mobility-limited. Mobility is set by graphene domain size, which is set by Ni island geometry during RTA graphitisation at 850–1050°C.

### Simulation 2 — Optical load retention under continuous 1550 nm flux
**Tools:** Quantum ESPRESSO (epsilon.x) + Python rate equation model
**Question:** Does continuous photon flux during inference generate sufficient carriers in graphene to shift the Fermi level across the Pauli blocking threshold?
**Why it matters:** Paper 3's 10-year retention claim is extrapolated from electrical lifetime testing without optical load. This is the architecture's primary open question.

### Simulation 3 — Write pulse electrostatic crosstalk at 3–5 µm cell pitch
**Tools:** FEniCS (open source) or COMSOL
**Question:** Does a 65 fJ write pulse applied to a TiN electrode produce sufficient fringe field to partially switch adjacent ferroelectric cells?
**Why it matters:** The 3–5 µm pitch target in Paper 3 has not been validated against crosstalk.

---

## How simulation outputs feed back into Paper 4

| Simulation | Output | Prior updated |
|------------|--------|---------------|
| Sim 1 | Graphene domain size vs Ni island diameter | Route F mobility prior |
| Sim 2 | Max optical power for retention | Paper 3 retention boundary |
| Sim 3 | Minimum safe cell pitch | Paper 3 array density specification |

---

## Contact

Nils Haaland
nhaaland@yahoo.com
Solbakken Research Initiative (Independent)

If you are running one of these simulations or have adjacent results in the literature, please get in touch. There is no funding to offer. The value exchange is a concrete application context for the computational work and co-authorship on any paper that uses these results.
