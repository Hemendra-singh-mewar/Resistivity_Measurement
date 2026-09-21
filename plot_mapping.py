"""Generate proposed silicon resistivity coordinates and a four-panel figure.

Usage: python plot_mapping.py --output outputs
All positions are probe-array centres, not individual probe contacts.
"""
from pathlib import Path
import argparse
import csv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import numpy as np

SAMPLES = {
    'S01': {'diameter': 42.7, 'height': 30.0, 'extra_radii': [], 'extra_heights': []},
    'S02': {'diameter': 100.0, 'height': 100.0,
            'extra_radii': [35.0], 'extra_heights': [50.0, 75.0, 90.0]},
}
COMMON_RADII = [8.5, 15.0]
COMMON_HEIGHTS = [7.5, 15.0, 22.5]
FACE_ANGLES = np.arange(0, 360, 45)
LATERAL_ANGLES = [0, 90, 180, 270]


def make_coordinates():
    """Use one sample-fixed frame: face A z=0, face B z=height.

    Viewed towards face A, +y is R0, +x is right and positive z goes
    into the sample. Theta increases clockwise from +y in that view.
    Coordinates for face B remain in this frame, not a reversed view.
    """
    rows = []
    def add(sample, surface, point, radius, angle, z, matched):
        theta = np.deg2rad(angle) if angle is not None else 0.0
        rows.append({
            'sample_id': sample, 'surface': surface, 'point_id': point,
            'matched_location': int(matched), 'r_mm': radius,
            'theta_deg': '' if angle is None else angle,
            'x_mm': round(radius*np.sin(theta), 6),
            'y_mm': round(radius*np.cos(theta), 6), 'z_mm': z,
        })
    for name, sample in SAMPLES.items():
        for face, z in [('A', 0.0), ('B', sample['height'])]:
            add(name, face, 'C', 0.0, None, z, True)
            rings = list(zip(['I', 'O'], COMMON_RADII))
            rings += [(f'E{k+1}_', r) for k, r in enumerate(sample['extra_radii'])]
            for prefix, radius in rings:
                for number, angle in enumerate(FACE_ANGLES, 1):
                    add(name, face, f'{prefix}{number}', radius, int(angle), z,
                        radius in COMMON_RADII)
        for level, z in enumerate(COMMON_HEIGHTS + sample['extra_heights'], 1):
            for suffix, angle in zip('abcd', LATERAL_ANGLES):
                add(name, 'lateral', f'L{level}{suffix}', sample['diameter']/2,
                    angle, z, z in COMMON_HEIGHTS)
    return rows


def validate(rows):
    """Check actual geometry and the coordinate matching used for comparison."""
    ids = [(r['sample_id'], r['surface'], r['point_id']) for r in rows]
    assert len(ids) == len(set(ids)), 'Duplicate point identifiers'
    for r in rows:
        sample = SAMPLES[r['sample_id']]
        assert 0 <= r['z_mm'] <= sample['height']
        assert r['r_mm'] <= sample['diameter']/2
        if r['surface'] != 'lateral':
            assert r['r_mm'] < sample['diameter']/2
    for surface in ['A', 'B', 'lateral']:
        matched = []
        for name in SAMPLES:
            points = [r for r in rows if r['sample_id'] == name
                      and r['surface'] == surface and r['matched_location']]
            # Face B has a different z because sample thickness differs.
            # Lateral points share theta and z, but lie at different radii.
            keys = ('point_id','theta_deg','z_mm') if surface == 'lateral' else ('point_id','r_mm','theta_deg')
            matched.append({tuple(r[k] for k in keys) for r in points})
        assert matched[0] == matched[1], f'Unmatched coordinates: {surface}'


def make_figure(rows, output):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                         'axes.linewidth': .7, 'pdf.fonttype': 42,
                         'ps.fonttype': 42})
    fig, axes = plt.subplots(2, 2, figsize=(9.5, 9))
    for column, (name, sample) in enumerate(SAMPLES.items()):
        ax = axes[0, column]
        ax.add_patch(Circle((0,0), sample['diameter']/2,
                            facecolor='none', edgecolor='black', lw=1))
        for radius in COMMON_RADII + sample['extra_radii']:
            ax.add_patch(Circle((0,0), radius, fill=False,
                                edgecolor='.65', lw=.6, ls=':'))
        for matched in [True, False]:
            points = [r for r in rows if r['sample_id'] == name
                      and r['surface'] == 'A' and bool(r['matched_location']) == matched]
            if points:
                ax.scatter([r['x_mm'] for r in points], [r['y_mm'] for r in points],
                           s=20, marker='o' if matched else 's',
                           facecolors='black' if matched else 'none',
                           edgecolors='black', linewidths=.8, zorder=3)
        R = sample['diameter']/2
        ax.annotate('R0',xy=(0,R),xytext=(0,R+5),ha='center',fontsize=8,
                    arrowprops={'arrowstyle':'-', 'lw':.7})
        ax.set(xlim=(-58,58),ylim=(-58,60),xlabel='x (mm)',ylabel='y (mm)')
        ax.set_aspect('equal');ax.set_xticks([-50,-25,0,25,50]);ax.set_yticks([-50,-25,0,25,50])
        ax.set_title(f'({"ab"[column]}) {name}: Ø {sample["diameter"]:g} mm, thickness {sample["height"]:g} mm\nEnd face A',fontsize=10)
        ax.axhline(0,color='.85',lw=.5,zorder=0);ax.axvline(0,color='.85',lw=.5,zorder=0)

        ax = axes[1,column]
        ax.add_patch(Rectangle((-20,0),310,sample['height'],facecolor='.97',edgecolor='.5',lw=.7))
        for matched in [True,False]:
            points = [r for r in rows if r['sample_id'] == name
                      and r['surface'] == 'lateral' and bool(r['matched_location']) == matched]
            if points:
                ax.scatter([r['theta_deg'] for r in points], [r['z_mm'] for r in points],
                           s=20,marker='o' if matched else 's',
                           facecolors='black' if matched else 'none',edgecolors='black',linewidths=.8,zorder=3)
        for level, z in enumerate(COMMON_HEIGHTS+sample['extra_heights'],1):
            ax.axhline(z,color='.8',lw=.5,ls=':',zorder=0)
            ax.text(281,z,f'L{level}',fontsize=7,va='center')
        ax.set(xlim=(-25,315),ylim=(-3,105),xlabel='Angular position, θ (degrees)',ylabel='Height from face A, z (mm)')
        ax.set_xticks(LATERAL_ANGLES);ax.set_yticks([0,7.5,15,22.5,30,50,75,90,100])
        ax.tick_params(axis='y',labelsize=8)
        ax.set_title(f'({"cd"[column]}) {name}: lateral surface',fontsize=10)
    handles = [plt.Line2D([],[],marker='o',color='black',ls='none',ms=4,label='Matched positions'),
               plt.Line2D([],[],marker='s',color='black',markerfacecolor='none',ls='none',ms=4,label='Additional positions')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.02),ncol=2,frameon=False)
    fig.subplots_adjust(left=.09,right=.97,bottom=.11,top=.94,hspace=.35,wspace=.30)
    fig.savefig(output/'measurement_layout.pdf')
    fig.savefig(output/'measurement_layout.png',dpi=300)
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('outputs'))
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    rows=make_coordinates();validate(rows)
    with (args.output/'measurement_coordinates.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    make_figure(rows,args.output)
    for name in SAMPLES:
        print(f'{name}: {sum(r["sample_id"]==name for r in rows)} planned positions')
    print(f'Figure and coordinates written to {args.output.resolve()}')


if __name__ == '__main__':
    main()
