import sys
import os
import json
import shutil
import subprocess
import hashlib
import re

def execute_cmd(command):
    if "md5(" in command and ")" in command:
        res = re.findall(r'md5\(.*?\)', command)
        for item in res:
            # item: md5(1)
            # value: 1
            # hashdata: c4ca4238
            value = item.replace("md5(", "")
            value = value[:-1]
            hashdata = hashlib.md5(value.encode()).hexdigest()
            hashdata = hashdata[:8]
            command = command.replace(item, hashdata)

    command_trip = command.strip()
    if command_trip.startswith("export "):
        # "export PATH=$PATH:{BUILD}/compiler/w64devkit/bin"
        # Remove export from command: 
        command_without_export = ((command_trip.split("export"))[1]).strip() # PATH=$PATH:{BUILD}/compiler/w64devkit/bin

        # Get the variable name:
        variable_name = (command_without_export.split("="))[0] # PATH

        # Remove variable name from command
        command_without_export = command_without_export.replace(f'{variable_name}=', "") # $PATH:{BUILD}/compiler/w64devkit/bin

        if f':${variable_name}:' in command_without_export: # in the middle
            print("in the middle")
        elif f'${variable_name}:' in command_without_export: # in the left
            remain_command = (command_without_export.split(f'${variable_name}:'))[1] # {BUILD}/compiler/w64devkit/bin
            if variable_name in os.environ:
                os.environ[variable_name] = os.environ[variable_name] + ";" + remain_command
            else:
                os.environ[variable_name] = remain_command
        elif f':${variable_name}' in command_without_export: # in the right
            remain_command = (command_without_export.split(f':${variable_name}'))[0] # {BUILD}/compiler/w64devkit/bin
            if variable_name in os.environ:
                os.environ[variable_name] = remain_command + ";" + os.environ[variable_name]
            else:
                os.environ[variable_name] = remain_command
        else:
            os.environ[variable_name] = command_without_export
    else:
        os.system(command)
