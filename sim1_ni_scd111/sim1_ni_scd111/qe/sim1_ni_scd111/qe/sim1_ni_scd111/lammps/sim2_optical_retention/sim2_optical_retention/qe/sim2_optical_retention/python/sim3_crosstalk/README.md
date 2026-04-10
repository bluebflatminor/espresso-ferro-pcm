# Simulation 3 — Write Pulse Electrostatic Crosstalk

## Files

### `fenics/sim3_crosstalk.py`
FEniCS finite element simulation of write pulse electrostatics combined
with Landau-Khalatnikov polarisation dynamics. Computes switching fraction
in adjacent cells. Falls back to analytical approximation if FEniCS
is not installed.

## Installation

```bash
# Option A: FEniCS via conda (recommended)
conda create -n fenics-env -c conda-forge fenics mshr
conda activate fenics-env
pip install numpy matplotlib scipy

# Option B: Docker
docker run -ti -v $(pwd):/home/fenics/shared fenicsproject/stable

# Option C: Analytical only (no FEniCS required)
pip install numpy matplotlib scipy
python sim3_crosstalk.py --no-fenics
