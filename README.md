# Silicon resistivity mapping

I put together this script to plan the resistivity measurements on our two silicon samples for ET-CRISTAL. The idea is to compare measurements at the same radii and angles on both samples, then add a few more positions to cover the larger one.

The figure and coordinate table show the proposed measurement locations. We still need to agree on the final spacing and contact arrangement with the measurement laboratory.

## Measurement layout

![Proposed resistivity measurement positions](outputs/measurement_layout.png)

[Download the figure as a PDF](outputs/measurement_layout.pdf) · [Download the coordinates](outputs/measurement_coordinates.csv)

## Samples

| Sample | Diameter | Thickness | Points on both end faces | Points on the lateral surface | Total |
| --- | --- | --- | --- | --- | --- |
| S01 | 42.7 mm | 30 mm | 34 | 12 | 46 |
| S02 | 100 mm | 100 mm | 50 | 24 | 74 |

These totals do not include repeated measurements or measurements with a different probe orientation.

## How I have chosen the positions

### Flat end faces

Both samples have a measurement at the centre and eight equally spaced positions on each of two rings:

- Inner ring: 8.5 mm radius.
- Outer ring: 15 mm radius.
- Angular spacing: 45°.

This gives 17 positions on each face. The larger sample has another eight positions at a radius of 35 mm, giving 25 positions per face.

I have kept the first two radii identical so we can compare corresponding locations. The extra ring lets us check the part of the larger sample that lies beyond the smaller sample's radius.

The plan is to repeat these measurements on both end faces.

### Lateral surface

On both samples, I have placed measurement points at heights of 7.5, 15 and 22.5 mm from face A. At each height, there are four positions around the cylinder: 0°, 90°, 180° and 270°.

For the larger sample, I have added rows at 50, 75 and 90 mm to cover the rest of its height.

We will need to check whether the probes can make reliable contact on the curved surface before including these measurements in the final plan.

## Running the script

The script uses Python 3.10 or later, with NumPy and Matplotlib.

From the project folder, install the dependencies and run:

```bash
python -m pip install -r requirements.txt
python plot_mapping.py --output outputs
```

If you prefer to use a virtual environment, create one first:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or on Linux/macOS:

```bash
source .venv/bin/activate
```

Then run the installation and plotting commands above.

## Output files

The script saves three files in `outputs`:

- `measurement_layout.pdf`: a vector figure for the note or a presentation.
- `measurement_layout.png`: a 300 dpi image.
- `measurement_coordinates.csv`: the coordinates of all 120 proposed locations.

The two end-face plots use the same scale, as do the two lateral plots. Filled circles show the positions chosen for comparison between samples. Open squares show the additional positions on the larger sample.

I have kept most point labels out of the figure to make it easier to read. The full identifiers are in the CSV.

## Coordinates and reference direction

I use the centre of face A as the origin. Looking towards face A:

- R0 points upwards, along +y.
- +x points to the right.
- +z runs into the sample, towards face B.
- The angle increases clockwise from R0.

The coordinates are calculated as:

```text
x = r sin(theta)
y = r cos(theta)

Face A: z = 0
Face B: z = sample thickness
```

The angle is left blank for the centre point.

Face B uses the same coordinates fixed to the sample. If we turn the cylinder over about the y axis, its visible layout is mirrored left to right. We should keep track of this reference using the holder or a photograph, without marking the optical surfaces.

## Point labels

| Label | Position |
| --- | --- |
| C | Centre |
| I1 to I8 | Ring at 8.5 mm |
| O1 to O8 | Ring at 15 mm |
| E1_1 to E1_8 | Extra ring at 35 mm on S02 |
| L1 | Lateral row at 7.5 mm |
| L2 | Lateral row at 15 mm |
| L3 | Lateral row at 22.5 mm |
| L4 | Extra lateral row at 50 mm |
| L5 | Extra lateral row at 75 mm |
| L6 | Extra lateral row at 90 mm |

For the end faces, points 1 to 8 correspond to angles of 0°, 45°, 90°, 135°, 180°, 225°, 270° and 315°.

For the lateral surface, suffixes `a`, `b`, `c` and `d` correspond to 0°, 90°, 180° and 270°.

Each measurement is identified by its sample, surface and point. For example:

```text
S01 / A / I3
S02 / lateral / L4b
```

The `matched_location` column identifies the positions selected for comparison. On the end faces, these share the same radius and angle. On the lateral surfaces, they share the same height and angle, although the cylinder radii differ.

## Things to agree before measuring

Each plotted point represents the centre of the probe arrangement. The individual contacts will occupy some space around it, so the final positions depend on the probe spacing and orientation.

Before starting, we should agree on:

- Clearance from the edges and bevels.
- Any cleaning or contact preparation.
- How to protect the polished surfaces.
- Corrections for sample thickness and geometry.
- Whether lateral measurements are practical.
- A few repeat measurements to check reproducibility.

Matching the coordinates will help us compare the samples, but it will not remove the effects of their different dimensions. It also does not mean that the points came from equivalent locations in the original ingot.

These measurements will give us information from the accessible surfaces. They will not, by themselves, provide a complete map of the interior.

Alongside the results, we should record the temperature, lighting, current, voltage, settling time, probe arrangement, surface preparation and measurement uncertainty.

## Changing the plan

The dimensions and measurement positions are defined near the top of `plot_mapping.py`:

```python
SAMPLES
COMMON_RADII
COMMON_HEIGHTS
FACE_ANGLES
LATERAL_ANGLES
```

Changing these values and running the script again updates the figure and coordinate table.

The script checks for duplicate point identifiers, positions outside the samples and consistency between the locations selected for comparison. It only generates the geometry; it does not calculate resistivity or electrical correction factors.

Once we have established the procedure at ambient temperature, we can use these measurements as a baseline for planning the cryogenic tests in our laboratory.
