def start_file(f):
    f.write('<svg xmlns="http://www.w3.org/2000/svg">\n')

def end_file(f):
        f.write('</svg>\n')
    
def write_layer(f, lines):
    for line in lines:
        f.write('<line x1="%f" y1="%f" x2="%f" y2="%f" stroke-width=".5" stroke="red" />\n' % (
                line[0][0], line[0][1], line[1][0], line[1][1]))
