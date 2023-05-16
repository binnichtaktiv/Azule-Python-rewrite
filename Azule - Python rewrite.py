import os
import shutil
import subprocess
import platform
import time
import patoolib


deb_file = r"C:\Users\jonas\Downloads\Telegram Desktop\com.dvntm.youtubeplus_2.3_iphoneos-arm.deb"
output_dir = r"C:\Users\jonas\Desktop"

print("[-i] Specify the IPA to patch")
print("[-o] Specify an output directory")
print("[-f] Specify the files or tweaks")
print("[-n] Specify a name for the Output IPA")

def extract_deb(deb_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    patoolib.extract_archive(deb_file, outdir=output_dir)

    data_file = None
    for file in os.listdir(output_dir):
        if file.startswith("data.tar"):
            data_file = os.path.join(output_dir, file)
            break

    if data_file:
        patoolib.extract_archive(data_file, outdir=output_dir)
        os.remove(data_file)
    else:
        pass

deb_file = "/Users/jonasb./Desktop/azule test/ytcl.deb"
output_dir = "/Users/jonasb./Desktop/azule test"

extract_deb(deb_file, output_dir)

def find_dylib_files(path):
    dylib_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.dylib'):
                dylib_files.append(os.path.join(root, file))
    return dylib_files

extracted_dir = os.path.join(output_dir, 'Library')
extract_deb(deb_file, extracted_dir)

dylib_files = find_dylib_files(extracted_dir)

temp_dir = os.path.join(output_dir, 'temp')
os.makedirs(temp_dir, exist_ok=True)

for dylib_file in dylib_files:
    shutil.copy(dylib_file, temp_dir)

shutil.rmtree(extracted_dir)

dylib_files = find_dylib_files(extracted_dir)