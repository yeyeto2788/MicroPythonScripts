import os

TOOLS_DIR = os.path.dirname(__file__)
PROJECTS_DIR = os.path.join(os.path.dirname(TOOLS_DIR), "projects")

COMMANDS = []
for root_dir, directories, files in os.walk(PROJECTS_DIR):
    if root_dir.endswith("code"):
        for file in files:
            if file.endswith(".py"):
                command = f"python {os.path.join(TOOLS_DIR, 'uncomment_and_upload.py')}"
                command += f" --input {os.path.join(root_dir, file)} --output {os.path.join(root_dir.replace('code', 'release'), file)}\n"
                COMMANDS.append(command)

with open(os.path.join(TOOLS_DIR, "obfuscate.sh"), "w") as file_out:
    file_out.writelines(COMMANDS)