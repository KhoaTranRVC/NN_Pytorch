import sys
import os
import json
import shutil
import subprocess
import hashlib
import re

from Common.BaseClass import BaseClass
from Utility import RunCommand

class OptionsLoop(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)
        self.repo = None

    def fill_array(self, index, nol, out_array, process_array):
        if index < nol - 1:
            loop = "LOOP" + (str)(index + 1)

            # Convert loop to MD5
            if "md5(" in (self.json_data["Input"][loop]) and ")" in (self.json_data["Input"][loop]):
                cur_loop = (self.json_data["Input"][loop])
                cur_loop = cur_loop.replace("md5(", "")
                cur_loop = cur_loop[:-1]
                cur_loop = cur_loop.split()
                temp_cur_loop = []
                for item in cur_loop:
                    hashdata = hashlib.md5(item.encode()).hexdigest()
                    hashdata = hashdata[:8]
                    temp_cur_loop.append(hashdata)
                cur_loop = temp_cur_loop
            else:
                cur_loop = (self.json_data["Input"][loop]).split()

            for item in cur_loop:
                out_array.append({f'{loop}[]': item})
                self.fill_array(index + 1, nol, out_array, process_array)
            if out_array: out_array.pop()
        else:
            loop = "LOOP" + (str)(index + 1)

            # Convert loop to MD5
            if "md5(" in (self.json_data["Input"][loop]) and ")" in (self.json_data["Input"][loop]):
                cur_loop = (self.json_data["Input"][loop])
                cur_loop = cur_loop.replace("md5(", "")
                cur_loop = cur_loop[:-1]
                cur_loop = cur_loop.split()
                temp_cur_loop = []
                for item in cur_loop:
                    hashdata = hashlib.md5(item.encode()).hexdigest()
                    hashdata = hashdata[:8]
                    temp_cur_loop.append(hashdata)
                cur_loop = temp_cur_loop
            else:
                cur_loop = (self.json_data["Input"][loop]).split()

            for item in cur_loop:
                process_array_one = out_array.copy()
                process_array_one.append({f'{loop}[]': item})
                process_array.append(process_array_one)
                # print(process_array_one)
            if out_array: out_array.pop()

    def execute(self):
        cwd = os.getcwd()
        os.chdir(self.json_data["Input"]["WORKDIR"])

        combine_array = []
        process_array = []
        combine_array_len = 0
        next_pos = 0
        numofloop = (int)(self.json_data["Input"]["NumberOfLoop"])

        self.fill_array(0, numofloop, combine_array, process_array)
        
        for items in process_array:
            for command in self.json_data["Action"]:
                none_loop_cmd = True
                for item in items:
                    str_bef = "{" + list(item.keys())[0] + "}"
                    str_after = list(item.values())[0]
                    command_after = command.replace(str_bef, str_after)
                   
                    if (command_after != command):
                        none_loop_cmd = False
                        RunCommand.execute_cmd(command_after)
                        
                if none_loop_cmd:
                    RunCommand.execute_cmd(command)
                    
        os.chdir(cwd)
