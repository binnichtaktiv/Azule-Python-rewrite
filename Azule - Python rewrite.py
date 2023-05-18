import os
import shutil
import platform
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

    if os.name == 'nt':
        file_paths = shlex.split(file_paths_input, posix=False)
    else:
        file_paths = shlex.split(file_paths_input)

    for path in file_paths:
        patoolib.extract_archive(path, outdir=deb_tmp, verbosity=-1)
        data_tar_file = None
        for file in os.listdir(deb_tmp):
            if file.startswith("data.tar"):
                data_tar_file = os.path.join(deb_tmp, file)
                break
        if data_tar_file:
            patoolib.extract_archive(data_tar_file, outdir=deb_tmp, verbosity=-1)
            os.remove(data_tar_file)
    clear_terminal()

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