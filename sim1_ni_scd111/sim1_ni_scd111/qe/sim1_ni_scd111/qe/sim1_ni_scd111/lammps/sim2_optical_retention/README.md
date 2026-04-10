# Simulation 2 — Optical Load Retention Under 1550 nm Flux

## Files

### `qe/graphene_hfo2_optical.in`
Quantum ESPRESSO pw.x + epsilon.x input for optical conductivity of graphene
on Al2O3/Al:HfO2 substrate as a function of carrier density n*.

### `python/sim2_retention.py`
Rate equation model for steady-state photocarrier density under continuous
1550 nm waveguide illumination. Feeds from QE epsilon.x outputs.
Runs standalone with placeholder sigma values if QE not available.

## Workflow

**Step 1 — QE optical conductivity sweep:**
```bash
# For each carrier density in {0, 1e11, 5e11, 1e12, 1.18e13} cm-2
# Set tot_charge in graphene_hfo2_optical.in accordingly

mpirun -np 32 pw.x -in graphene_hfo2_optical.in | tee scf.out
mpirun -np 32 epsilon.x -in graphene_hfo2_optical.in | tee epsilon.out

# Extract Im[epsilon] at 0.80 eV
# Update SIGMA_TABLE in sim2_retention.py
