import os
import shutil
import subprocess
import platform

print("[-i] Specify the IPA to patch")
print("[-o] Specify an output directory")
print("[-f] Specify the files or tweaks")
print("[-n] Specify a name for the Output IPA")

def extract_deb(deb_file, output_dir):
    if platform.system() == 'Linux':
        subprocess.call(['dpkg-deb', '-x', deb_file, output_dir])
    elif platform.system() == 'Darwin':
        subprocess.call(['sudo', 'ditto', '-x', '-k', deb_file, output_dir])
    # elif platform.system() == 'Windows':
    # yeah idk - manual extraction needed

def find_dylib_files(path):
    dylib_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.dylib'):
                dylib_files.append(os.path.join(root, file))
    return dylib_files

deb_file_path = '/home/bsnw/Downloads/com.ps.ytuhd_1.3.5-1_iphoneos-arm64(1).deb'
output_dir = '/home/bsnw/Downloads'

extracted_dir = os.path.join(output_dir, 'extracted_deb')
extract_deb(deb_file_path, extracted_dir)

dylib_files = find_dylib_files(extracted_dir)

temp_dir = os.path.join(output_dir, 'temp')
os.makedirs(temp_dir, exist_ok=True)

for dylib_file in dylib_files:
    shutil.copy(dylib_file, temp_dir)

print(dylib_files)
