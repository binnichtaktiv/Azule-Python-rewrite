import os
import shutil
import subprocess
import platform
import time
import patoolib
import shlex


def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')

print("Azule: A CLI tool used to inject iOS jailbreak tweaks into jailed iOS apps.")
print("Features: \nInject debs/dylibs\nmore features will be added later")

start = input("\n\nenter 'start' to start injecting.\n")
clear_terminal()


if start == 'start':
    file_paths_input = input("Enter the path to your .deb/.dylib. (There can be several at once):\n ")
    clear_terminal()
    output_dir = input("Enter an output path:\n")
    deb_tmp = os.path.join(output_dir, "deb_tmp")

    if not os.path.exists(deb_tmp):
        os.makedirs(deb_tmp)

    file_paths = shlex.split(file_paths_input)
    for path in file_paths:
        patoolib.extract_archive(path, outdir=deb_tmp, verbosity=-1)
    clear_terminal()

    def extract_deb(deb_file, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        data_file = None
        for file in os.listdir(output_dir):
            if file.startswith("data.tar"):
                data_file = os.path.join(output_dir, file)
                break

        if data_file:
            patoolib.extract_archive(data_file, outdir=output_dir, verbosity=-1)
            os.remove(data_file)

    for path in file_paths:
        extract_deb(path, deb_tmp)

    def find_dylib_files(path):
        dylib_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.dylib'):
                    dylib_files.append(os.path.join(root, file))
        return dylib_files

    dylib_files = find_dylib_files(deb_tmp)

    temp_dir = os.path.join(output_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    for dylib_file in dylib_files:
        shutil.copy(dylib_file, temp_dir)

    dylib_files = find_dylib_files(deb_tmp)
    shutil.rmtree(deb_tmp)
