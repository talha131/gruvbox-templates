#!/usr/bin/env python3
import sys
import glob
import os.path

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

replace = {}
styles = []
with open('color.table') as f:
    styles = f.readlines()

for style in styles:
    split = style.split()
    if len(split) < 2:
        continue

    colorTitle = split[0]
    htmlHex = split[1]

    val = split[-1] if split[-1][0] == '#' else split[1]
    
    rgb = hex_to_rgb(val)
    r = rgb[0] / 255
    g = rgb[1] / 255
    b = rgb[2] / 255
    replacement = '{} {} {}'.format(r, g, b)

    replace['$({})'.format(colorTitle)] = replacement
    replace['$({}#red)'.format(colorTitle)] =  r
    replace['$({}#green)'.format(colorTitle)] = g
    replace['$({}#blue)'.format(colorTitle)] = b

    replace['#({})'.format(colorTitle)] = htmlHex

for fname in glob.glob('templates/*'):
    final_content = ""
    with open(fname) as f:
        content = f.read()
        for k,v in replace.items():
            content = content.replace(k, '{}'.format(v));

        final_content = content

    with open(os.path.join('output', os.path.basename(fname)), 'w') as f:
        f.write(final_content)

