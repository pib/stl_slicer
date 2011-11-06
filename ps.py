# millimeters to points
PPMM = 360.0 / 127.0


def start_file(f, width, height):
    f.write('%!PS\n')
    f.write('<</PageSize [%f %f]>> setpagedevice\n' % (width * PPMM, height * PPMM))
    f.write('0 %f translate\n' % (height * PPMM))
    f.write('/mt /moveto load def\n')
    f.write('/moveto { neg mt } bind def\n')
    f.write('/lt /lineto load def\n')
    f.write('/lineto { neg lt } bind def\n')
    f.write('/Courier 12 selectfont\n')


def end_file(f):
    f.write('\n')


def write_layer_paths(f, paths, number=None):
    if not len(paths):
        return
    f.write('save\n')
    f.write('newpath\n')
    #if number is not None:
        #f.write('<text text-anchor="middle" font-size="2" fill="none" stroke-width="0.1" stroke="blue">%d</text>\n' % number)

    for path in paths:
        f.write('%f %f moveto\n' % (path[0][0] * PPMM, path[0][1] * PPMM))
        for point in path[1:]:
            f.write('%f %f lineto ' % (point[0] * PPMM, point[1] * PPMM))
        f.write('\n')
    f.write('closepath\nstroke\nshowpage\n')
    f.write('restore\n')
