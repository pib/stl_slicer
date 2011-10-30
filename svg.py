def start_file(f):
    f.write('<svg xmlns="http://www.w3.org/2000/svg">\n')


def end_file(f):
        f.write('</svg>\n')


def write_layer_lines(f, lines):
    for line in lines:
        f.write('<line x1="%f" y1="%f" x2="%f" y2="%f" stroke-width=".1" stroke="red" />\n' % (
                line[0][0], line[0][1], line[1][0], line[1][1]))


def write_layer_paths(f, paths, number=None):
    f.write('<g>\n')
    if number is not None:
        f.write('<text text-anchor="middle" font-size="2" fill="none" stroke-width="0.1" stroke="blue">%d</text>\n' % number)

    for path in paths:
        f.write('<path fill="none" stroke-width="0.1" stroke="red" d="M %f %f' % path[0])
        for point in path[1:]:
            f.write(' L %f %f' % point)
        f.write('" />\n')
    f.write('</g>\n')
