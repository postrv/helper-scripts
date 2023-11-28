"""
Helper script to write the contents of all files with a given extension in a given directory to a text file
for easy upload to ChatGPT as reference material.
"""

import os
import argparse


def should_ignore_dir(dir_path):
    ignore_dirs = {'node_modules', 'debug', '_next', '.next'}
    return any(ignore in dir_path.split(os.sep) for ignore in ignore_dirs)


def find_files(directory, extensions):
    for root, dirs, files in os.walk(directory):
        if should_ignore_dir(root):
            continue
        for file in files:
            if file.endswith(extensions):
                yield os.path.join(root, file)


def write_file_contents(file_path, output_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        output_file.write(f"// File: {file_path}\n")
        output_file.write(file.read())
        output_file.write("\n\n")


def main():
    parser = argparse.ArgumentParser(
        description="Find specific file types in a given directory, excluding node_modules, "
                    "debug, and _next directories, and write their contents to a text file.")
    parser.add_argument("directory", type=str, help="Path to the directory to search")
    parser.add_argument("-o", "--output", default="output.txt", help="Output file name (default: output.txt)")
    args = parser.parse_args()

    extensions = ('.rs', '.ts', '.tsx', '.js', '.jsx', '.sql', '.html', '.css')

    if not os.path.exists(args.directory):
        print(f"Error: The directory '{args.directory}' does not exist.")
        return

    with open(args.output, 'w') as output_file:
        for file_path in find_files(args.directory, extensions):
            write_file_contents(file_path, output_file)


if __name__ == "__main__":
    main()
