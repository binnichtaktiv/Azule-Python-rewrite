import os
import shutil
import subprocess
import platform







print("[-i] Specify the the IPA to patch")
print("[-o] Specify an output directory")
print("[-f] Specify the files or tweaks")
print("[-n] Specify a name for the Output iPA")


def extract_deb(deb_file, output_dir):
    if platform.system() == 'Linux':
        subprocess.call(['dpkg-deb', '-x', deb_file, output_dir])
    elif platform.system() == 'Darwin':
        subprocess.call(['sudo', 'ditto', '-x', '-k', deb_file, output_dir])
    elif platform.system() == 'Windows':
        subprocess.call(['7z', 'x', '-y', '-odefaultdir', deb_file])

# Funktion zum Suchen von Dateien, die mit ".dylib" enden
def find_dylib_files(path):
    dylib_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.dylib'):
                dylib_files.append(os.path.join(root, file))
    return dylib_files

# Pfad zur .deb-Datei
deb_file_path = 'path/to/deb_file.deb'

# Ausgabeordner für die extrahierten Dateien
output_dir = 'path/to/output_dir'

# Extrahieren der .deb-Datei in den Ausgabeordner
extract_deb(deb_file_path, output_dir)

# Suchen nach Dateien, die mit ".dylib" enden, im Ausgabeordner
dylib_files = find_dylib_files(output_dir)

# Drucken der gefundenen Dateien
print(dylib_files)