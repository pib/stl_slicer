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
    f.write('1 0 0 setrgbcolor\n')
    f.write('0.1 setlinewidth\n')


def end_file(f):
    f.write('\n')

offset = 0
def write_layer_paths(f, paths, number=None):
    global offset
    if not len(paths):
        return
    f.write('save\n')
    f.write('newpath\n')

    if number is not None:
        for path in paths:
            x_avg = sum(d[0] for d in path[1:]) / (len(path)-1) * PPMM
            y_avg = sum(d[1] for d in path[1:]) / (len(path)-1) * PPMM
            f.write('0 0 1 setrgbcolor\n')
            f.write('%f %f moveto ' % (x_avg, y_avg))
            f.write('(%s) dup stringwidth pop 2 div neg 0 rmoveto false charpath\n' % (number))
        f.write('closepath\nstroke\nrestore\nsave\nnewpath\n')

    for path in paths:
        f.write('%f %f moveto\n' % (path[0][0] * PPMM, path[0][1] * PPMM))
        for point in path[1:]:
            f.write('%f %f lineto ' % (point[0] * PPMM, point[1] * PPMM))
        f.write('\n')
    f.write('closepath\nstroke\nshowpage\n')
    f.write('restore\n')
