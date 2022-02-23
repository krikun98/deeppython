import random
from datetime import date
from image_gen_deeppython import graph


def generate_line():
    return [random.randint(0, 100) for _ in range(10)]


def generate_matrix():
    return [generate_line() for _ in range(10)]


def preamble():
    return """
%! Author = kriku
%! Date = {}

% Preamble
\\documentclass[11pt]{{article}}

% Packages
\\usepackage{{amsmath}}
\\usepackage{{tikz}}

""".format(date.today().strftime("%d/%m/%Y"))


def wrap_document(content):
    return "\\begin{document}\n\n" + content + "\\end{document}\n\n"


def wrap_image(path):
    return "\\input{" + path + "}\n\n"


def wrap_center(content):
    return "\\begin{center}\n\n" + content + "\\end{center}\n\n"


def wrap_tabular(content, columns):
    return "\\begin{tabular}{|" + (" c |" * columns) + "}\n" + content + "\\end{tabular}\n\n"


def hline():
    return "\\hline\n"


def line_transform(line):
    return " & ".join([str(item) for item in line]) + "\\\\\n" + hline()


def matrix_transform(table):
    return hline() + "\n".join([line_transform(line) for line in table]) + "\n"


def matrix_to_table(table):
    return wrap_center(wrap_tabular(matrix_transform(table), len(table[0])))


def create_document(content):
    return preamble() + wrap_document(content)


if __name__ == "__main__":
    with open("artifacts/test_array.tex", "w") as file:
        file.write(create_document(matrix_to_table(generate_matrix())))
    with open("artifacts/test_image.tex", "w") as file:
        graph.main(graph="artifacts/plot.pgf")
        file.write(create_document(wrap_image("plot.pgf")))
