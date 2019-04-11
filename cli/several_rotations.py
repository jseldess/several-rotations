"""Create a new file with a random permutation of lines from a source text file,
formatted to resemble the stanzaic structure of IN, the first poem of
SEVERAL ROTATIONS, with options to set a max number of lines, set a max line
length, break lines into sections, use only unique lines, randomly skip lines,
and/or remove a specified number of words from the start of lines.

Help: python3 several_rotations.py --help

Example usage:

Generate file with unique lines:
    python3 several_rotations.py -u -sf source.txt
Generate file with duplicate lines:
    python3 several_rotations.py -sf source.txt
Generate file with unique lines, skipping lines randomly:
    python3 several_rotations.py -u -r -sf source.txt
Generate file with duplicate lines, skipping lines randomly:
    python3 several_rotations.py -r -sf source.txt
Generate file with 10 unique lines, skipping lines ramdonly:
    python3 several_rotations.py -u -r -ml 10 -sf source.txt
Generate file with 10 unique lines, removing 2 words from start of each:
    python3 several_rotations.py -u -ml 10 -rw 2 -sf source.txt
Generate file with 100 unique lines, in sections of 10, skipping lines randomly:
    python3 several_rotations.py -u -r -ml 100 -ls 10 -sf source.txt
Generate file with 100 unique lines of 70 characters or less, in sections of 10:
    python3 several_rotations.py -u -ml 100 -mll 70 -ls 10 -sf source.txt
Generate file with 10 sections of 10 unique lines, skipping lines randomly:
    python3 several_rotations.py -u -r -mll 70 -ms 5 -ls 10 -sf source.txt
"""

import argparse
import os
import re
import random
from time import gmtime, strftime

parser = argparse.ArgumentParser(
    description="""Create a new file with a random permutation of lines from a
    source text file, formatted to resemble the stanzaic structure of IN, the
    first poem of SEVERAL ROTATIONS, with options to set a max number of lines,
    set a max line length, break lines into sections, use only unique lines,
    randomly skip lines, and/or remove a specified number of words from the start
    of lines.""")
parser.add_argument("-sf", "--source_file",
                    help="Source text file (default: source.txt)",
                    default = "source.txt")
parser.add_argument("-d", "--new_file_dir",
                    help="""Path to the directory where the new file will be
                    created (default: generated_files)""",
                    default="generated_files")
parser.add_argument("-u", "--unique_lines",
                    action="store_true",
                    help="""Use each unique line from the source file only once
                    (default: False)""")
parser.add_argument("-r", "--random_skip",
                    action="store_true",
                    help="Randomly skip writing lines (default: False)")
parser.add_argument("-ls", "--lines_per_section", type=int,
                    help="Number of lines of text per section")
parser.add_argument("-ms", "--max_sections", type=int,
                    help="Max number of sections")
parser.add_argument("-ml", "--max_lines", type=int,
                    help="Max number of lines of text in total")
parser.add_argument("-mll", "--max_line_length", type=int,
                    help="Max number of characters per line")
parser.add_argument("-rw", "--remove_words", type=int,
                    help="Number of words to remove from the start of a line")
args = parser.parse_args()

# Create a new directory for generated files, if it doesn't exist.
if not os.path.exists(args.new_file_dir):
    os.makedirs(args.new_file_dir)

# Create a new file named with the current timestamp and flags passed.
filename = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
if args.unique_lines:
    filename += "_unique"
if args.random_skip:
    filename += "_skip"
if args.lines_per_section:
    filename += "_sectionlines" + str(args.lines_per_section)
if args.max_sections:
    filename += "_maxsections" + str(args.max_sections)
if args.max_lines:
    filename += "_maxlines" + str(args.max_lines)
if args.max_line_length:
    filename += "_maxlinelength" + str(args.max_line_length)
if args.remove_words:
    filename += "_remove" + str(args.remove_words)
filename += "_py.txt"
new_file = open(os.path.join(args.new_file_dir, filename), "a")

# Read source file and store its lines as a list of strings in source.
with open(args.source_file) as file:
    source = file.readlines()
    lines_seen = set()
    total_lines = 0
    lines_in_section = 0
    section = 1
    if args.lines_per_section:
        new_file.write(str(section) + "\n\n\n")
    while len(source) > 0:
        # If --max_lines is passed, break out of the loop
        # as soon as the max lines have been written.
        if args.max_lines:
            if total_lines == args.max_lines:
                break
        # If --lines_per_section is passed, create new section
        # after specified number of lines.
        if args.lines_per_section:
            if lines_in_section == args.lines_per_section:
                if args.max_sections:
                    if section == args.max_sections:
                        break
                section += 1
                new_file.write("\n" + str(section) + "\n\n\n")
                lines_in_section = 0
        # Randomly select a line and remove it from source.
        line = random.choice(source)
        source.remove(line)
        if not line.isspace():
            if args.max_line_length:
                if len(line) > args.max_line_length:
                    continue
            # If --random_skip is passed, randomly skip the line
            # and continue the next iteration of the loop.
            # To increase the chance of skips, add 1s to the list.
            if args.random_skip and random.choice([0, 1]) == 1:
                print("Skip line")
                continue
            # If --remove_words is passed, remove the specified number
            # of words from the start of the line.
            if args.remove_words:
                remove_expr = "^" + ("\W*\w+" * args.remove_words) + "\W*"
                line = re.sub(remove_expr, "\n", line)
            # If --unique_lines is passed, check if the line was
            # seen in a previous iteration. If not, write the line
            # to new_file and add it to lines_seen.
            if args.unique_lines:
                if line.strip().lower() in lines_seen:
                    continue
                lines_seen.add(line.strip().lower())
            new_file.write(line)
            print("Write line")
            total_lines += 1
            # Radomly write 0, 1, 2, 3, or 4 empty lines
            # to new_file, with 0 weighted heavier.
            new_file.write(random.choice([
            "", "", "", "", "\n", "\n\n", "\n\n\n", "\n\n\n\n"]))
            if args.lines_per_section:
                lines_in_section += 1

print("File {} created".format(filename))
print("Total lines: {}".format(total_lines))
