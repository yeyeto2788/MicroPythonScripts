#!/usr/bin/env python3
"""
Script to automate the process of cleaning micropython files and uploading them
onto the board.

It uses:
pyminifier==2.1

"""

import os
import argparse
import platform
import subprocess
import importlib.util

module_name = 'pyminifier'
module_spec = importlib.util.find_spec(module_name)

if module_spec is None:
    print(f"Couldn't find the {module_name} module")
    exit(-1)
else:
    token_utils = importlib.import_module(f'{module_name}.token_utils', module_name)
    minification = importlib.import_module(f'{module_name}.minification', module_name)
    obfuscate = importlib.import_module(f'{module_name}.obfuscate', module_name)

PY_EXTENSION = '.py'


class CleanOptions:
    """
    Abstract class to define the options used for the pyminifier module.

    """

    def __init__(self, bln_obfuscate=False):
        """
        Simple constructor method to define the properties of the object.

        If we want to obfuscate the code we can do it by setting the `bln_obfuscate`
        argument to True so the code size will also be smaller.

        It is recommended to test first without doing so.

        Args:
            bln_obfuscate: Whether we want to obfuscate the code.
        """
        # Use tabs instead of spaces
        self.tabs = False
        # Obfuscate all code
        self.obfuscate = bln_obfuscate
        self.obf_classes = False
        self.obf_functions = False

        self.nominify = False
        self.obf_variables = False
        self.obf_builtins = False
        self.obf_import_methods = False
        self.replacement_length = 1
        self.use_nonlatin = False


def clean_file(source_file_name: str, destination_file_name: str = "", bln_print: bool = 0):
    """
    Perform a cleaning action by removing all types of DocStrings on the code.

    Args:
        source_file_name: name of the file_name to be parsed.
        destination_file_name: name of the destination file_name.
        bln_print: Print lines of file_name.

    Returns:
        None
    """
    _file = source_file_name

    module = os.path.split(_file)[1]
    module = ".".join(module.split('.')[:-1])

    source = open(_file).read()
    tokens = token_utils.listified_tokenizer(source)

    # Change option below `bln_obfuscate` to True if you want to make the code even smaller.
    options = CleanOptions(bln_obfuscate=False)

    if not options.nominify:  # Perform minification
        source = minification.minify(tokens, options)
        # Convert back to tokens in case we're obfuscating
        tokens = token_utils.listified_tokenizer(source)

    # Perform obfuscation if any of the related options were set
    if options.obfuscate:
        identifier_length = int(options.replacement_length)
        name_generator = obfuscate.obfuscation_machine(
            identifier_length=identifier_length
        )
        obfuscate.obfuscate(module, tokens, options)

    result = token_utils.untokenize(tokens)

    if bln_print:
        print(result)

    if destination_file_name != "":
        with open(destination_file_name, 'w') as destination_file:
            destination_file.write(result)

        destination_file.close()


def push_file(file_path: str, serial_port: str):
    """
    Execute the commands on the terminal to load the script on the board.

    Args:
        file_path: String with the file_name path to be flash on the board.
        serial_port: String with the serial port to which the board is connected to.

    """

    if serial_port != '':

        print('Flashing \'{}\'.\n'.format(file_path))

        command_arguments = ['sudo', 'ampy', '--port', serial_port, 'put', file_path]

        if os.name == "posix" and platform.system() == "Linux":
            subprocess.call(command_arguments)

        elif os.name == "nt" and platform.system() == "Windows":
            subprocess.call(command_arguments[1:])

        else:
            print("Hhmm, seems like you have MacOs and we haven't implement the code for this yet.")


def process_files(python_files: list, projects_input: str, projects_output: str,
                  print_output: bool, port: str, upload: bool):
    """
    Given a list files minify and/or obfuscate them, create new files if required and flash
    them to the board.

    Args:
        python_files: Files to be processed.
        projects_input: Folder where files are taken from.
        projects_output: Folder where files are written on.
        print_output:
        port: Port to be used by `ampy` tool.
        upload: condition to upload file onto the board.

    Returns:
        None
    """
    for file_name in python_files:
        current_input = os.path.join(projects_input, file_name)
        msg = "Result:\n\n"

        if projects_output != '':
            current_output = os.path.join(projects_output, file_name)

            if current_output.endswith(PY_EXTENSION):
                msg = f"The file {current_output} will be written with the following:\n\n"
        else:
            current_output = projects_output

        print(msg)
        clean_file(current_input, current_output, bln_print=print_output)
        print("\n\n")

        if upload:
            push_file(current_output, port)


def build_path_args(path: str) -> (str, str):
    """Given a path extract the filename and the directory if possible.

    Args:
        path: Path on which apply the splitting.

    Returns:
        (file_directory, filename)
    """
    files_dir = path

    if os.path.isdir(path):
        python_files = [py_file for py_file in os.listdir(path) if py_file.endswith(PY_EXTENSION)]

    else:
        os.path.isfile(path)
        filedir, filename = os.path.split(path)
        python_files = [filename]
        files_dir = filedir

    return files_dir, python_files


def main(options):
    """Set variables needed to delete docstring and obfuscate the script before flashing them onto
    the board.

    Args:
        options: `parser.parse_args()` arguments.

    Returns:
        None.
    """
    print_output = options.print
    projects_input = os.path.abspath(os.path.normpath(options.input))

    if not os.path.exists(projects_input):
        print('Seems like the input directory does not exists.')
        exit(-1)

    if options.output != '':
        output_dir, _ = build_path_args(options.output)
        projects_output = os.path.abspath(os.path.normpath(output_dir))

        if not os.path.exists(projects_output):
            os.makedirs(projects_output)
    else:
        projects_output = options.output

    input_dir, input_files = build_path_args(projects_input)
    process_files(input_files, input_dir, projects_output, print_output, options.port, options.upload)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Script to automate the process of cleaning micropython files and'
                    ' uploading them onto the board.')

    parser.add_argument('-o', '--output', action='store', nargs='?',
                        default='', type=str, help='Output directory.')
    parser.add_argument('-i', '--input', action='store', nargs='?',
                        default='', type=str, help='Input file or directory.')
    parser.add_argument('-p', '--port', action='store', nargs='?',
                        default='', type=str, help='Port to flash files.')
    parser.add_argument('-u', '--upload', action='store', nargs='?',
                        default=False, type=bool, help='Upload file(s) to board.')
    parser.add_argument('--print', action='store', nargs='?',
                        default=True, type=bool, help='Print result.')

    args = parser.parse_args()

    if args.input and not args.print and (args.output != ''):
        print("Please provide an output destination file directory.")
        exit(-1)

    elif args.input:
        main(options=args)
        exit(0)

    else:
        print('Please review usage of the application below.')
        print(parser.print_help())
        exit(-1)
