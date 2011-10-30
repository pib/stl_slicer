import argparse
import os.path
import math

from stl import parse
import svg

X = 0
Y = 1
Z = 2


def find_line_plane_intersection(a, b, z):
    """ Find where a line between two points intersects a given
    axis-aligned plane
    """
    dx = a[X] - b[X]
    dy = a[Y] - b[Y]
    dz = a[Z] - b[Z]
    z_z0 = z - b[Z]

    xi = z_z0 * (dx / dz) + b[X]
    yi = z_z0 * (dy / dz) + b[Y]
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
        if line[0] != line[1]:
            lines.append(line)
    return lines


class LineMap(object):
    def __init__(self, lines):
        map = {}
        for line in lines:
            for point in line:
                key = self._key(point)
                line_set = map.setdefault(key, [])
                line_set.append(line)
        self._map = map

    def _key(self, point):
        return '{0:.8},{1:.8}'.format(*point)

    def has_lines(self):
        if self._map:
            return True
        else:
            return False

    def _pop_other_line(self, key, line):
        for point in line:
            if self._key(point) == key:
                continue
            other_point = point
            break

        key = self._key(other_point)
        lines = self._map[key]
        lines.remove(line)
        if len(lines) == 0:
            del self._map[key]

        return other_point

    def take_line(self):
        """ Take an arbitrary line out of the internal map
        """
        for key, lines in self._map.iteritems():
            line = lines.pop()
            if len(lines) == 0:
                del self._map[key]

            self._pop_other_line(key, line)
            return line

    def next_point(self, point):
        """ Return the next endpoint of an unused line which starts at
        the given point.

        Also removes the used line from the internal map.
        """
        key = self._key(point)
        lines = self._map.get(key, None)
        if lines is None:
            return None

        line = lines.pop()
        if len(lines) == 0:
            del self._map[key]

        other_point = self._pop_other_line(key, line)

        return other_point


def path_lines(lines):
    """ Convert a list of lines into paths
    """
    unused = LineMap(lines)

    paths = []
    while unused.has_lines():
        path = unused.take_line()

        point = unused.next_point(path[-1])
        while point:
            path.append(point)
            point = unused.next_point(point)
        paths.append(path)
    return paths


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
    z = minz
    while z <= maxz:
        lines = slice_shape_at(facets, z)
        paths = path_lines(lines)
        svg.write_layer_paths(f, paths)
        z += args.thickness
    svg.end_file(f)
    f.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='.stl file to slice')
    parser.add_argument('-t', '--thickness', help='thickness of each slice, in mm', default=1, type=float)
    args = parser.parse_args()

    main(args)
