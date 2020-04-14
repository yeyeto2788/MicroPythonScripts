#! /usr/bin/env python3
import argparse
import os
import shutil
import zipfile

log = False


def verbose(*arguments, **kwargs):
    """Dummy function to log output on commands if needed."""
    global log

    if log:
        print(*arguments, **kwargs)


def get_release_files(projects_dir: str) -> dict:
    """Walk over the repo and find the release files.

    It will look over the folder named 'release' all files within that folder.

    Args:
        projects_dir: Directory where to look files in.

    Returns:
        Dictionary containing the following structure:
        'project_name':{
            'file1.ext': {
                'from': 'dir/from/which/to/copy/file/from'
                'to': ''dir/from/which/to/copy/file/to''
            }
        }
    """
    destination = ''
    project_release = dict()

    for root_dir, directories, files in os.walk(projects_dir):

        if root_dir.endswith('release'):
            project_name = os.path.basename(os.path.dirname(root_dir))
            project_release[project_name] = dict()

            for file in files:
                project_release[project_name][file] = dict()
                original_file_dir = os.path.join(root_dir, file)
                project_release[project_name][file]["from"] = original_file_dir
                filename = os.path.basename(original_file_dir)
                destination_dir = os.path.join(destination, project_name, filename)
                project_release[project_name][file]["to"] = destination_dir

    return project_release


def generate_zip(files: list, destination: str):
    """Iterate over the list of files copied and generate a zip files with them"""
    verbose("-" * 20)
    verbose("Zipping files.".upper())
    zip_dir = os.path.join(destination, 'release.zip')

    with zipfile.ZipFile(zip_dir, 'w') as zip_obj:
        for file in files:
            inner_filename = os.path.join(
                os.path.basename(os.path.dirname(file)),
                os.path.basename(file)
            )
            verbose(f"Adding '{inner_filename}' into zip.")
            zip_obj.write(
                file,
                arcname=inner_filename
            )
    verbose("Done Zipping files.".upper())


def copy_files(data: dir, destination: str):
    files_copied = list()
    verbose("-" * 20)
    verbose("Copying files:".upper())

    for _, project_files in data.items():
        for _, files in project_files.items():
            destination_dir = os.path.join(destination, files['to'])
            os.makedirs(os.path.dirname(destination_dir), exist_ok=True)
            verbose(f"Copying file '{files['from']}' to '{destination_dir}'")
            shutil.copyfile(files['from'], destination_dir)
            files_copied.append(destination_dir)
    verbose("Done copying.".upper())

    return files_copied


def print_data(data: dict):
    print(f"We found '{len(data.keys())}' projects.\n")

    for project, files in data.items():
        print(f"'{project}' project has the following files:")
        [print(f"\t{file}") for file in files.keys()]


def main(options):
    global log
    repo_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    projects_dir = os.path.abspath(os.path.join(repo_dir, 'projects'))

    if options.verbose:
        log = True
    # Get all project release files.
    data = get_release_files(projects_dir)
    print_data(data)
    copied_files = None

    if options.output != "":
        destination = os.path.abspath(options.output)
        # Check if directory exists or not.
        if not os.path.exists(destination):

            try:
                verbose("-" * 20)
                verbose(f"Creating '{destination}' directory.")
                os.makedirs(destination, exist_ok=True)
            except Exception as exe_error:
                verbose("Something went wrong trying to create the destination directory.")
                raise exe_error
        # Only copy files if directory exists or if
        # no problem found creating destination directory.
        copied_files = copy_files(data, destination)

    if options.zip:
        # Check if there is at least one file copied in order
        # to invoke the zipping process.
        if copied_files is not None:
            generate_zip(copied_files, destination)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Script to generate the release of the projects so it can be easily upload'
                    'to the boards.')

    parser.add_argument('-o', '--output', action='store', nargs='?',
                        default='', type=str, help='Output directory.')
    parser.add_argument('-z', '--zip', action='store', nargs='?',
                        default=False, type=bool, help='Make zip file.')
    parser.add_argument('-v', '--verbose', action='store', nargs='?',
                        default=False, type=bool, help='Verbose output.')

    args = parser.parse_args()

    try:
        main(options=args)
        exit(0)

    except Exception as exec_error:
        print(f"An error has occurred: {exec_error}\nArgs used: {args}")
        print('\n\nPlease review usage of the application below.')
        print(parser.print_help())
        exit(-1)
