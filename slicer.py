import argparse
import os.path
import math

from stl import parse
import svg

X = 0
Y = 1
Z = 2

def find_line_plane_intersection(a, b, z):
    """ Find where a line between two points intersects a given axis-aligned plane """
    dx = a[X] - b[X]
    dy = a[Y] - b[Y]
    dz = a[Z] - b[Z]
    z_z0 = z - b[Z]

    xi = z_z0 * (dx / dz) + b[X]
    yi = z_z0 * (dy / dz) + b[Y]
    #print '% 6.2f, % 6.2f, % 6.2f to % 6.2f, % 6.2f, % 6.2f -> % 6.2f, % 6.2f' % (a[0], a[1], a[2], b[0], b[1], b[2], xi, yi)
    return (xi, yi)

def tri_above_below(tri, z):
    # FIXME: how to handle when all Zs are equal to z
    above = []
    below = []
    for point in tri:
        if point[Z] < z:
            below.append(point)
        elif point[Z] >= z:
            above.append(point)
    return above, below

def slice_shape_at(facets, z):
    lines = []
    for tri in facets:
        above, below = tri_above_below(tri, z)
        if not above or not below:
            continue

        line = []
        for a in above:
            for b in below:
                line.append(find_line_plane_intersection(a, b, z))
        lines.append(line)
    return lines

def main(args):
    facets = parse(open(args.file, 'rb'))
    minz = 99999
    maxz = -99999
    for facet in facets:
        for point in facet:
            minz = min(minz, point[Z])
            maxz = max(maxz, point[Z])

    svg_filename = os.path.splitext(os.path.basename(args.file))[0] + '.svg'
    f = open(svg_filename, 'w')

    svg.start_file(f)
    for z in range(int(math.floor(minz)), int(math.ceil(maxz)), 1):
        lines = slice_shape_at(facets, z)
        svg.write_layer(f, lines)
    svg.end_file(f)
    f.close()
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='.stl file to slice')
    parser.add_argument('-t', '--thickness', help='thickness of each slice')
    args = parser.parse_args()

    main(args)
