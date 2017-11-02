import os

path = "./lightning-bolt.jpg"
fname = "test-proxies"

with open(fname + '.tex', 'w') as f:
    f.write('\\documentclass[11pt] {article}\n')
    f.write('\\usepackage[margin=0.3in]{geometry}\n')
    f.write('\\usepackage{graphicx}\n')
    f.write('\\usepackage{pdflscape}\n\n')
    f.write('\\begin{document}\n')
    f.write('\\begin{landscape}\n\n')
    for i in range(8):
        f.write('\\includegraphics[width=6.3cm]{' + path + '}\n')
    f.write('\n')
    f.write('\\end{landscape}\n')
    f.write('\\end{document}\n')

# if the os call executes with a return status of 0
if os.system('pdflatex -halt-on-error -interaction=nonstopmode ' + fname + ' >> /dev/null') == 0:
    print("PDF created")
else:
    print("Something broke... No output file created")

os.system('rm {}.aux {}.log'.format(fname, fname)) # clean up auxilary files
os.system('rm {}.tex'.format(fname)) # clean up the tex file
