# SEVERAL ROTATIONS CLI

This directory contains the command-line utility used to generate the starting
points for the poems IF and ELSE and to generate the poem 2019-04-06-11:05:32 UTC
(unmodified and named for its generation time), based on the remnants of the
process of writing the poem IN, all for the book SEVERAL ROTATIONS.

## Synopsis

Create a new file with a random permutation of lines from a source text file,
formatted to resemble the stanzaic structure of IN, the first poem of
SEVERAL ROTATIONS, with options to set a max number of lines, set a max line
length, break lines into sections, use only unique lines, randomly skip lines,
and/or remove a specified number of words from the start of lines.

## Options

``` shell
-h, --help            show this help message and exit
-sf SOURCE_FILE, --source_file SOURCE_FILE
                      Source text file (default: source.txt)
-d NEW_FILE_DIR, --new_file_dir NEW_FILE_DIR
                      Path to the directory where the new file will be
                      created (default: generated_files)
-u, --unique_lines    Use each unique line from the source file only once
                      (default: False)
-r, --random_skip     Randomly skip writing lines (default: False)
-ls LINES_PER_SECTION, --lines_per_section LINES_PER_SECTION
                      Number of lines of text per section
-ms MAX_SECTIONS, --max_sections MAX_SECTIONS
                      Max number of sections
-ml MAX_LINES, --max_lines MAX_LINES
                      Max number of lines of text in total
-mll MAX_LINE_LENGTH, --max_line_length MAX_LINE_LENGTH
                      Max number of characters per line
-rw REMOVE_WORDS, --remove_words REMOVE_WORDS
                      Number of words to remove from the start of a line
```

## Examples

``` shell
# Generate file with unique lines:
python3 several_rotations.py -u -sf source.txt

# Generate file with duplicate lines:
python3 several_rotations.py -sf source.txt

# Generate file with unique lines, skipping lines randomly:
python3 several_rotations.py -u -r -sf source.txt

# Generate file with duplicate lines, skipping lines randomly:
python3 several_rotations.py -r -sf source.txt

# Generate file with 10 unique lines, skipping lines ramdonly:
python3 several_rotations.py -u -r -ml 10 -sf source.txt

# Generate file with 10 unique lines, removing 2 words from start of each:
python3 several_rotations.py -u -ml 10 -rw 2 -sf source.txt

# Generate file with 100 unique lines, in sections of 10, skipping lines randomly:
python3 several_rotations.py -u -r -ml 100 -ls 10 -sf source.txt

# Generate file with 100 unique lines of 70 characters or less, in sections of 10:
python3 several_rotations.py -u -ml 100 -mll 70 -ls 10 -sf source.txt

# Generate file with 10 sections of 10 unique lines, skipping lines randomly:
python3 several_rotations.py -u -r -mll 70 -ms 5 -ls 10 -sf source.txt
```
