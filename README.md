# Silicon resistivity mapping

Reproducible coordinates and a scientific figure for proposed resistivity measurements on two cylindrical silicon samples. This repository describes a measurement plan, not measured resistivity results.

## Samples and proposed coverage

| Sample | Diameter | Thickness | End faces | Lateral surface | Total |
| --- | --- | --- | --- | --- | --- |
| S01 | 42.7 mm | 30 mm | 17 points on each face | 12 points | 46 |
| S02 | 100 mm | 100 mm | 25 points on each face | 24 points | 74 |

Both samples share a centre point and eight positions at each radius of 8.5 and 15 mm. S02 has an additional ring at 35 mm. Angular spacing is 45 degrees.

Both sidewalls have points at heights of 7.5, 15 and 22.5 mm from face A, at angles of 0, 90, 180 and 270 degrees. S02 has additional rows at 50, 75 and 90 mm. Totals exclude repeat readings and changes in probe orientation.

## Run the script

Use Python 3.10 or later. From this directory:

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or on Linux/macOS:

```bash
source .venv/bin/activate
```

Install the plotting dependencies and generate the files:

```bash
python -m pip install -r requirements.txt
python plot_mapping.py --output outputs
```

The script generates:

- `outputs/measurement_layout.pdf`: vector figure for LaTeX or printing.
- `outputs/measurement_layout.png`: 300 dpi preview.
- `outputs/measurement_coordinates.csv`: all 120 planned positions, including both end faces.

The four panels use equal physical scales within each pair so that the different sample sizes and shared measurement locations can be compared directly. Filled circles are matched positions; open squares are additional positions. Detailed point identifiers are in the CSV to avoid crowding the figure.

## Coordinate convention

The sample-fixed origin is the centre of face A. Viewed towards face A, R0 is +y (up), +x is right and +z runs into the cylinder towards face B. Theta increases clockwise from R0 in this view:

```text
x = r sin(theta)
y = r cos(theta)
face A: z = 0
face B: z = sample thickness
```

The centre has no defined theta, so its CSV angle is blank. Face B retains the same sample-fixed x and y coordinates. If the sample is turned over about its y axis, the visible face-B layout is mirrored left to right relative to face A. Record the physical datum with a holder or photograph, without marking an optical surface.

### Point identifiers

- `C`: centre.
- `I1` to `I8`: 8.5 mm ring.
- `O1` to `O8`: 15 mm ring.
- `E1_1` to `E1_8`: additional 35 mm ring on S02.
- Ring point numbers 1 to 8 correspond to 0, 45, 90, 135, 180, 225, 270 and 315 degrees.
- Lateral rows `L1`, `L2`, `L3`: 7.5, 15, 22.5 mm.
- Additional rows `L4`, `L5`, `L6`: 50, 75, 90 mm.
- Lateral suffixes `a`, `b`, `c`, `d`: 0, 90, 180, 270 degrees.

A unique record is the combination of sample ID, surface and point ID, for example `S01 / A / I3` or `S02 / lateral / L4b`.

For matched end-face locations, r and theta agree, but face-B z differs because the thicknesses differ. For matched lateral locations, z and theta agree, but the cylinder radii differ. The `matched_location` column records these nominal comparisons, not physically identical sampling volumes or equivalent original ingot positions.

## Experimental checks before adopting the grid

All dots denote proposed probe-array centres, not individual electrical contacts. Agree with the measurement laboratory on probe spacing and orientation, edge clearance, thickness and boundary corrections, contact method, surface preparation and the suitability of sidewall measurements. This script does not calculate current flow, resistivity corrections or sampling depth.

The lateral surface should only be measured if reliable contact and a suitable interpretation are possible. Matching coordinates does not remove geometry effects. Measurements on accessible surfaces do not provide a complete three-dimensional map of the interior. Record temperature, lighting, current, voltage, settling time, probe geometry, surface preparation, uncertainty and repeat readings with the acquired results.

Edit `SAMPLES`, `COMMON_RADII`, `COMMON_HEIGHTS` and the angle lists in `plot_mapping.py` to change the plan. The script checks point uniqueness, sample bounds and the nominal matching between samples before exporting.

## Suggested caption

Proposed resistivity measurement positions on two cylindrical silicon samples. Panels (a) and (b) show face A; corresponding positions are repeated on face B. Panels (c) and (d) show lateral positions as angle and height from face A. Filled circles indicate nominally matched positions and open squares show additional coverage on the larger sample. All symbols denote probe-array centres. The layout is provisional and subject to probe geometry and surface access.

## Add this project to GitHub

Create an empty repository named `silicon-resistivity-mapping`. Choose private visibility if the plan is for internal work. Do not initialise the remote with a README if using the commands below.

From this project directory:

```bash
git init
git add .
git commit -m "Add proposed silicon resistivity measurement grid"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/silicon-resistivity-mapping.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub account name. Alternatively, upload the project files using GitHub's web interface. No repository has been published as part of preparing this project.
