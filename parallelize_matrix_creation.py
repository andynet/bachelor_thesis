#!/usr/bin/python3

import sys
import subprocess

def load_lines(file):

    with open(file) as f:
        lines = f.readlines()

    return lines


def calculate_phages_per_node(start, number_of_phages, comparison_per_node):

    current_comparisons = 0
    for i in range(number_of_phages-start, -1, -1):
        current_comparisons += i
        last_phage = number_of_phages - i + 1
        if current_comparisons > comparison_per_node:
            return last_phage

    return number_of_phages

if len(sys.argv) != 4:
    print('Usage:', sys.argv[0], '<pairs> <genes.conversion> <phages.list>')
    exit()

# <editor-fold desc="constants for our clusters">
nodes = 10
# </editor-fold>

phages = load_lines(sys.argv[3])
number = len(phages)
print('Comparing', number, 'phages.')

comparison_per_node = sum(range(number))/nodes
print('Comparisons per node:', comparison_per_node)

start_phage = 0
for i in range(nodes):

    end_phage = calculate_phages_per_node(start_phage, number, comparison_per_node)
    command = './create_similarity_matrix.py {} {} {} {} {}'.format(sys.argv[1], sys.argv[2], sys.argv[3],
                                                                    start_phage, end_phage)
    qsub_command = 'echo "' + command + '" | qsub -l thr=16 -cwd -N phages' + str(i)
    print(qsub_command)
    print('Comparisons made:', sum(range(number)[number-start_phage:number-end_phage:-1]))
    subprocess.call(qsub_command, shell=True)

    start_phage = end_phage
