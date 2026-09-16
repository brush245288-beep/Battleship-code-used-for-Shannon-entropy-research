# Entropy-Based Decision Making in Battleship

Python implementations developed for my 2025 BEng Mechanical Engineering
individual project:

**Exploring Data Acquisition and Decision Analysis Through Information Entropy by Using Battleship**

The project uses a simulated Battleship environment to investigate
information acquisition and decision-making under uncertainty.

A 14 × 14 playable board is used with randomly placed ships. The project
compares different targeting strategies, including random search,
local probability-based targeting after a hit, and global
permutation-based entropy analysis.

The code was developed iteratively for research experiments rather than as
a production software package. Some files therefore contain duplicated
implementations or earlier experimental versions and are retained to show
the development of the project.

## Repository Structure

### Core utilities

- `battleshipdata.py`
  - Defines ship dimensions used by the simulation.

- `chessboardgenerator.py`
  - Generates the NumPy board representation and coordinate labels.
  - Includes both 14 × 14 and 10 × 10 board variants.

- `battleRelateFunction.py`
  - Shared Battleship and entropy-analysis functions.
  - Includes:
    - ship-state updates;
    - random strike generation;
    - local ship-placement permutation calculation;
    - probability-map construction;
    - local/global entropy calculation;
    - entropy-based strike selection;
    - entropy plots;
    - Continuous Wavelet Transform (CWT) visualisation;
    - statistical comparison utilities.

### Main experiment scripts

- `local_probability_base.py`
  - Local probability targeting experiment.
  - Random search is used until a ship is found, after which possible
    continuations of the detected ship are evaluated.
  - Records local and global entropy during gameplay.

- `newglobal.py`
  - Experimental global permutation-based entropy implementation.
  - Enumerates feasible remaining ship placements over the full board and
    uses them to construct a spatial probability / entropy map.

- `Interactive Battleship.py`
  - Interactive Battleship prototype.
  - Allows manual coordinate input while displaying entropy-based suggested
    target locations and entropy heatmaps.

### Legacy / test scripts

- `newentropybase.py`
  - Earlier standalone implementation of the local entropy algorithm.
  - Contains functionality later separated into `battleRelateFunction.py`.
  - Retained as a development / legacy version.

- `runthroughgameboard.py`
  - Experimental script used to test full-board permutation counting and
    entropy heatmap generation.
  - Not intended as the primary program entry point.

## Main Algorithmic Ideas

### Local probability strategy

After a successful hit, the algorithm evaluates feasible horizontal and
vertical placements of the remaining ships around the observed hit
coordinates. These placements are accumulated into a probability map and
used to select subsequent targets.

### Global permutation strategy

For each remaining ship, all feasible placements on the current board are
enumerated. Cells receive weights according to how frequently they occur
in valid placements. The resulting distribution is converted into an
entropy map and can be used for target selection and visualisation.

### Entropy analysis

Binary Shannon entropy is used to quantify uncertainty associated with
candidate target locations. Entropy values are tracked throughout a game,
with additional visualisation using heatmaps and Continuous Wavelet
Transform (CWT).

## Requirements

The scripts use Python with the following main packages:

```bash
pip install numpy matplotlib scipy seaborn tabulate
```

## Running

For example, the local probability experiment can be run with:

```bash
python local_probability_base.py
```

The interactive prototype can be run with:

```bash
python "Interactive Battleship.py"
```

Some legacy and experimental scripts may require minor modification before
running and are included primarily to document the development process.

## Notes

This repository contains research prototype code produced during an
undergraduate individual project. The implementation evolved alongside the
research, so naming, structure, and code organisation are not intended to
represent a polished software library.

The accompanying dissertation provides the full methodology, mathematical
description, experimental results, and discussion.

## If the code is difficult to follow...

Don't worry — I also find parts of it difficult to read now.

This is archived undergraduate research code, and some parts were written very much in the spirit of "if it works, don't touch it."

For a clearer explanation of the main algorithms, it is probably better to start with the **Method** section of my BEng dissertation, where the overall logic and flowcharts are easier to follow. More detailed pseudocode is included in the **Appendix**.
