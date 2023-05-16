import os
import shutil
import subprocess
import platform
import time

#trash

deb_file = r"C:\Users\jonas\Downloads\Telegram Desktop\com.dvntm.youtubeplus_2.3_iphoneos-arm.deb"
output_dir = r"C:\Users\jonas\Desktop"
#trash

print("[-i] Specify the IPA to patch")
print("[-o] Specify an output directory")
print("[-f] Specify the files or tweaks")
print("[-n] Specify a name for the Output IPA")

def extract_deb(deb_file, output_dir):
    if platform.system() == 'Linux':
        subprocess.call(['dpkg-deb', '-x', deb_file, output_dir])
    elif platform.system() == 'Darwin':
        subprocess.call(['sudo', 'ditto', '-x', '-k', deb_file, output_dir])
    elif platform.system() == 'Windows':
        subprocess.call([r"C:\Program Files\7-Zip\7z.exe", "x", "-y", f"-o{output_dir}", deb_file])
        time.sleep(2)
        data_tar = output_dir + "\data.tar"
        subprocess.call([r"C:\Program Files\7-Zip\7z.exe", "x", "-y", f"-o{output_dir}", data_tar])
        os.remove(data_tar)

def find_dylib_files(path):
    dylib_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.dylib'):
                dylib_files.append(os.path.join(root, file))
    return dylib_files

deb_file_path = r'C:\Users\jonas\Downloads\Telegram Desktop\com.dvntm.youtubeplus_2.3_iphoneos-arm.deb'
output_dir = r'C:\Users\jonas\Desktop'

if platform.system == 'Windows':
    extracted_dir = os.path.join(output_dir, 'Library')
    extract_deb(deb_file_path, extracted_dir)

    dylib_files = find_dylib_files(extracted_dir)

    temp_dir = os.path.join(output_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    for dylib_file in dylib_files:
        shutil.copy(dylib_file, temp_dir)
        shutil.rmtree(extracted_dir)
else:
    extracted_dir = os.path.join(output_dir, 'extracted_deb')
    extract_deb(deb_file_path, extracted_dir)

    dylib_files = find_dylib_files(extracted_dir)

    temp_dir = os.path.join(output_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    for dylib_file in dylib_files:
        shutil.copy(dylib_file, temp_dir)
        shutil.rmtree(extracted_dir)
