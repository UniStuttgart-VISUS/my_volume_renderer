import sys, getopt
import matplotlib.pyplot as plt
import matplotlib as mpl
import csv
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# user input
inputfile = ''
outputfile = ''

min_value = 0.0
max_value = 1.0

caption = ''

horizontal = True
alpha = False

help_string = 'colorbar.py --input <inputfile> --output <outputfile> [--min <min value>] [--max <max value>] [--caption <captiontext>] [--vertical] [--rgba]'

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['help', 'input=', 'output=', 'min=', 'max=', 'caption=', 'vertical', 'rgba'])
except getopt.GetoptError:
    print(help_string)
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print(help_string)
        sys.exit()
    elif opt in ('-i', '--input'):
        inputfile = arg
    elif opt in ('-o', '--output'):
        outputfile = arg
    elif opt == '--min':
        min_value = float(arg)
    elif opt == '--max':
        max_value = float(arg)
    elif opt == '--caption':
        caption = arg
    elif opt == '--vertical':
        horizontal = False
    elif opt == '--rgba':
        alpha = True

if inputfile == '':
    print(help_string)
    sys.exit(2)
if outputfile == '':
    print(help_string)
    sys.exit(2)

orientation = 'horizontal'
width = 6
height = 1

if not horizontal:
    orientation = 'vertical'
    width = 1.1
    height = 6

# read colors
with open(inputfile, newline='') as csvfile:
    data = list(csv.reader(csvfile))

rgb = [tuple(float(j) for j in i[1:4]) for i in data[1:]]
rgba = [tuple(float(j) for j in i[1:]) for i in data[1:]]

# create color map
cmap_rgb = LinearSegmentedColormap.from_list('custom_map', rgb, N=np.shape(rgb)[0])
cmap_rgba = LinearSegmentedColormap.from_list('custom_map', rgba, N=np.shape(rgba)[0])

cmap = cmap_rgb
if alpha:
    cmap = cmap_rgba

# create color bar
fig, ax = plt.subplots(figsize=(width, height))

if horizontal:
    fig.subplots_adjust(bottom=0.5)
else:
    fig.subplots_adjust(right=0.5)

norm = mpl.colors.Normalize(vmin=min_value, vmax=max_value)

cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation=orientation)
cb1.set_label(caption)

fig.savefig(outputfile, format='pdf')
