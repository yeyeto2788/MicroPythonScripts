import os
import token
import tokenize
import platform
import subprocess


def clean_file(source_file_name, destination_file_name, bln_print=0):
    """

    Args:
        source_file_name: name of the file_name to be parsed.
        destination_file_name: name of the destination file_name.
        bln_print: Print lines of file_name.

    Returns:
        None
    """
    source = open(source_file_name)
    destination = open(destination_file_name, "w")

    prev_toktype = token.INDENT
    last_lineno = -1
    last_col = 0

    tokgen = tokenize.generate_tokens(source.readline)

    for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:

        if bln_print:
            print("{:>8} {:14} {!r:20} {!r}".format(
                tokenize.tok_name.get(toktype, toktype),
                "{:d}.{:d}-{:d}.{:d}".format(slineno, scol, elineno, ecol),
                ttext,
                ltext)
            )

        if slineno > last_lineno:
            last_col = 0

        if scol > last_col:
            destination.write(" " * (scol - last_col))

        if toktype == token.STRING and prev_toktype == token.INDENT:
            # Docstringcheck (Uncomment below to get a different result)
            # destination.write("#--")
            pass

        elif toktype == tokenize.COMMENT:
            # Comment check (Uncomment below to get a different result)
            # destination.write("")
            pass

        else:
            destination.write(ttext)

        prev_toktype = toktype
        last_col = ecol
        last_lineno = elineno

    # Close files
    source.close()
    destination.close()


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

    projects_py = os.path.normpath(os.path.join(project_path, "Code"))
    projects_output = os.path.normpath(os.path.join(project_path, "Release"))

    if not os.path.exists(projects_output):
        os.mkdir(projects_output)

    for file_name in os.listdir(projects_py):
        current_py = os.path.join(projects_py, file_name)
        current_output = os.path.join(projects_output, file_name)

        clean_file(current_py, current_output)
        print('Flashing \'{}\'.\n'.format(file_name))
        push_file(current_output, "/dev/ttyUSB0")

