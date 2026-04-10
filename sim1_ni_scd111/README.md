# Simulation 1 — Ni Island Formation and Graphene Nucleation on SCD(111)

## Files

### `qe/ni_scd111_relax.in`
Quantum ESPRESSO pw.x input for Ni adatom relaxation on H-terminated SCD(111).
Run this first to find the stable adsorption geometry.

### `qe/ni_diffusion_neb.in`
Quantum ESPRESSO neb.x input for Ni surface diffusion barrier.
Requires completed relax calculation. Uses climbing-image NEB.

### `lammps/ni_rta_md.in`
LAMMPS molecular dynamics for Ni island coarsening during RTA at 850–1050°C.
Uses ReaxFF force field (Ni/C/H parameterisation required — see notes below).

## Required inputs

**Pseudopotentials (QE):**
Download ONCV norm-conserving pseudopotentials for Ni, C, H from [PseudoDojo](http://www.pseudo-dojo.org/).
Set `PSEUDO_DIR` in input files to your local path.

**ReaxFF parameter file (LAMMPS):**
`ffield.reax.NiCH` — Zou et al. (2012) Ni-C parameterisation.
Available from the LAMMPS ReaxFF parameter repository.

**Substrate geometry:**
Generate `scd111_slab.data` using ASE:
```python
from ase.build import surface
from ase.io import write
slab = surface('diamond', (1,1,1), 6, vacuum=15.0)
slab.center(vacuum=15, axis=2)
write('scd111_slab.lammps', slab, format='lammps-data')
