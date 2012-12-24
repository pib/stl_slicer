def start_file(f, width, height):
    f.write("""<svg xmlns="http://www.w3.org/2000/svg"
      xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
      xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape">\n""")
    f.write('<sodipodi:namedview units="mm" />\n')


def end_file(f):
        f.write('</svg>\n')


def write_layer_lines(f, lines):
    for line in lines:
        f.write('<line x1="%f" y1="%f" x2="%f" y2="%f" stroke-width=".1" stroke="red" />\n' % (
                line[0][0], line[0][1], line[1][0], line[1][1]))


def write_layer_paths(f, paths, number=None):
    f.write(
        '<g inkscape:groupmode="layer" inkscape:label="Layer {0}" id="{0}">\n'.format(
            number))

    for path in paths:
        if number is not None:
            f.write('<g>\n')
            x_avg = sum(d[0] for d in path) / len(path)
            y_avg = sum(d[1] for d in path) / len(path)
            f.write('<text text-anchor="middle" '
                    'font-size="2" fill="none" stroke-width="0.1" stroke="blue" '
                    'x="%s" y="%s"'
                    '>%d</text>\n' % (x_avg, y_avg, number))

        f.write('<path fill="none" stroke-width="0.1" stroke="red" d="M %f %f' % path[0])
        for point in path[1:]:
            f.write(' L %f %f' % point)
        f.write('" />\n')

        if number is not None:
            f.write('</g>\n')
    f.write('</g>\n')
