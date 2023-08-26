import numpy as np
import math
import pandas as pd
from pathlib import Path
import json

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm, colors


def draw_wafer_plot(data, title):
    # some basic parameters
    r = 150
    w = 31.06
    h = 25.79
    offset = (1.32 - 2 * w, 2.59 + 4 * h)
    
    # notch
    s = 8
    notch_coords = np.array([[2*r, r - s/2], [2*r, r + s/2], [2*r - 0.5*s, r]])
    
    map_fdir = Path().absolute().parent
    df = pd.read_csv(map_fdir / 'dione_wafermap.csv')
    wm = {}
    for i, row in df.iterrows():
        wm[int(row['reticle'])] = row['x']/1000, row['y']/1000 # unit mm

    
    tested_rets = list(data.keys())
    vals = list(data.values())
    vmax = np.max(vals)
    vmin = np.min(vals)
    
    # get a colormap and a norm
    cmp = mpl.colormaps['RdBu_r']
    norm = colors.Normalize(vmin, vmax)
    
    # create all reticles
    rets = {}
    for id in range(len(wm)):
        x, y = r + wm[id][0] + offset[0], r + wm[id][1] + offset[1]
        if id in tested_rets:
            ret = plt.Rectangle((x, y), w, h, facecolor=cmp(norm(data[id])), edgecolor='k')
        else:
            ret = plt.Rectangle((x, y), w, h, facecolor='0.5', edgecolor='0')
        rets[id] = x, y, ret
    
    fig, ax = plt.subplots(figsize=(12, 8))
    wafer = plt.Circle((r, r), r, color='k', fill=False)
    notch = plt.Polygon(notch_coords, color='k', closed=True)
    ax.add_patch(wafer)
    ax.add_patch(notch)
    for id, ret in rets.items():
        ax.text(ret[0] + 0.2 * w, ret[1] + 0.8 * h, id, fontsize=10, weight='bold', ha='center', va='center')
        if id in tested_rets:
            l = data[id]
            ax.text(ret[0] + 0.5 * w, ret[1] + 0.2 * h, f'{l:.3f}', fontsize=10, ha='center', va='center')
        ax.add_patch(ret[2])
    ax.set_aspect("equal")
    ax.set_xlim([0, 2*r])
    ax.set_ylim([0, 2*r])
    ax.set_title(title, fontsize=14, weight='bold')
    ax.axis('off')
    fig.colorbar(cm.ScalarMappable(norm, cmp), ax=ax)
    plt.show()
