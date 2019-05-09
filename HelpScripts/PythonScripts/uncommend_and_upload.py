"""
Script to automate the process of cleaning micropython files and uploading them
onto the board.

It uses:
pyminifier==2.1

"""

import os
import platform
import subprocess

from pyminifier import minification, obfuscate, token_utils


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
        self.tabs = False
        self.obfuscate = bln_obfuscate
        self.obf_classes = False
        self.obf_functions = False
        self.nominify = False
        self.obf_variables = False
        self.obf_builtins = False
        self.obf_import_methods = False
        self.replacement_length = 1
        self.use_nonlatin = False


def clean_file(source_file_name: str, destination_file_name: str, bln_print: bool = 0):
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
        name_generator = obfuscate.obfuscation_machine(identifier_length=identifier_length)
        obfuscate.obfuscate(module, tokens, options)

    result = token_utils.untokenize(tokens)

    if bln_print:
        print(result)

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

    command_arguments = ['sudo', 'ampy', '--port', serial_port, 'put', file_path]

    if os.name == "posix" and platform.system() == "Linux":
        subprocess.call(command_arguments)
    elif os.name == "nt" and platform.system() == "Windows":
        subprocess.call(command_arguments[1:])
    else:
        print("Hhmm, seems like you have MacOs and we haven't implement the code for this yet.")


if __name__ == '__main__':
    project_path = os.path.normpath(
        input("Please type the directory from where code will be uncommented: \n>>>").rstrip()
    )

    projects_input = os.path.normpath(os.path.join(project_path, "Code"))
    projects_output = os.path.normpath(os.path.join(project_path, "Release"))

    if not os.path.exists(projects_output):
        os.mkdir(projects_output)

    python_files = [py_file for py_file in os.listdir(projects_input) if py_file.endswith('.py')]

    for file_name in python_files:
        current_py = os.path.join(projects_input, file_name)
        current_output = os.path.join(projects_output, file_name)

        clean_file(current_py, current_output)
        print('Flashing \'{}\'.\n'.format(file_name))
        push_file(current_output, "/dev/ttyUSB0")

