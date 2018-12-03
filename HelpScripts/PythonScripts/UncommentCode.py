import os
import platform
import subprocess


def uncomment(original_path: str, final_path: str) -> bool:
    """

    Args:
        original_path: String with the path of the .py file to be uncommented.
        final_path: String with the path to write the final export file.

    Returns:
        Boolean when the operation is done.
    """

    output_text = str()
    rm_all = None

    with open(original_path) as _file_handler:

        for line in _file_handler.readlines():

            if not rm_all and (line.strip().startswith('"""') or line.strip().startswith("'''")):
                rm_all = True
                continue

            if rm_all and (line.strip().endswith('"""') or line.strip().endswith("'''")):
                rm_all = False
                continue

            if rm_all:
                continue

            if line.strip().startswith('#'):
                continue

            elif not line.strip():
                continue

            else:
                output_text += line

    with open(final_path, 'w') as _file_handler:
        _file_handler.write(output_text)

    return True


def push_file(file_path: str, serial_port: str):
    """
    Execute the commands on the terminal to load the script on the board.

    Args:
        file_path: String with the file path to be flash on the board.
        serial_port: String with the serial port to which the board is connected to.

    """

    command_arguments = ['sudo', 'ampy', '--port', serial_port, 'put', file_path]

    if os.name == "posix" and platform.system() == "Linux":
        subprocess.call(command_arguments)
    elif os.name == "nt" and platform.system() == "Windows":
        subprocess.call(command_arguments[1:])
    else:
        print("mmmm, seems like you have MacOs and at the moment we haven't implement the code for this.")


if __name__ == '__main__':
    project_path = os.path.normpath(input("Please type the directory from where code will be uncommented: \n>>>").rstrip())

    projects_py = os.path.normpath(os.path.join(project_path, "Code"))
    projects_output = os.path.normpath(os.path.join(project_path, "Release"))

    if not os.path.exists(projects_output):
        os.mkdir(projects_output)

    for file in os.listdir(projects_py):
        current_py = os.path.join(projects_py, file)
        current_output = os.path.join(projects_output, file)

        uncomment(current_py, current_output)
        print('Flashing \'{}\'.\n'.format(file))
        push_file(current_output, "/dev/ttyUSB0")

