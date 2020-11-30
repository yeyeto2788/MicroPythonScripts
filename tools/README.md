# Tools

## Tools available

- `generate_releases.py` (WIP)
  Loop through all projects available on this repository and convert the files on the `code` folders into a stripped and short file with less characters, and create a `.zip` folder with all of them.

- `uncommend_and_upload.py` (DONE)
  Delete comments and try to make the scripts smaller and upload it to the board.

## Requirements

All needed requirements are listed on the `requirements.txt` file placed on this folder.

To use the tools just install them by executing the following commands from the root path of this cloned repository:

```shell
cd ./tools
pip install -r requirements.txt
chmod +x ./*.py
```
