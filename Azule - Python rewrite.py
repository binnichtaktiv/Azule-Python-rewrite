import os
import shutil
import subprocess
import platform
import argparse






print("[-i] Specify the the IPA to patch")
print("[-o] Specify an output directory")
print("[-f] Specify the files or tweaks")
print("[-n] Specify a name for the Output iPA")


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--arg1', nargs='+', help='Erstes Argument')
parser.add_argument('-i', '--arg2', nargs='+', help='Zweites Argument')
parser.add_argument('-r', '--arg3', nargs='+', help='Drittes Argument')

# Benutzereingabe abfragen
flags = input("Gib die Flags mit den Werten ein: ")

# args parsen
parsed_args, unknown = parser.parse_known_args(flags.split())

arg1 = parsed_args.arg1 if parsed_args.arg1 else []
arg2 = parsed_args.arg2 if parsed_args.arg2 else []
arg3 = parsed_args.arg3 if parsed_args.arg3 else []

print("Erstes Argument:", arg1)
print("Zweites Argument:", arg2)
print("Drittes Argument:", arg3)



def extract_deb(deb_file, output_dir):
    if platform.system() == 'Linux':
        subprocess.call(['dpkg-deb', '-x', deb_file, output_dir])
    elif platform.system() == 'Darwin':
        subprocess.call(['sudo', 'ditto', '-x', '-k', deb_file, output_dir])
    #elif platform.system() == 'Windows':
        # yeah idk - manual extraction needed

def find_dylib_files(path):
    dylib_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.dylib'):
                dylib_files.append(os.path.join(root, file))
    return dylib_files

deb_file_path = 'path/to/deb_file.deb'

output_dir = 'path/to/output_dir'

extract_deb(deb_file_path, output_dir)

dylib_files = find_dylib_files(output_dir)

print(dylib_files)