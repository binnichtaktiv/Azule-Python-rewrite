import os
import subprocess
import shutil
import patoolib
import shlex
import zipfile
import time
import plistlib 


def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear') 
        
def unzip_ipa(ipa_path):
    clear_terminal()
    file_name_no_ipa = os.path.basename(ipa_path)[:-4]
    zip_path = ipa_path.replace(".ipa", ".zip")

    if os.path.exists(ipa_path):
        os.rename(ipa_path, zip_path)
        print("iPA file successfully renamed to .Zip")
        time.sleep(1)
        clear_terminal()
    else:
        print("The .iPA file could not be found. Try again...")
        exit()

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(zip_path))

    payload_path = os.path.join(os.path.dirname(zip_path), "Payload")
    app_folder = os.listdir(payload_path)[0]
    app_path = os.path.join(payload_path, app_folder)
    return app_path, file_name_no_ipa, zip_path, payload_path

def zip_ipa(ipa_path, app_path, file_name_no_ipa, payload_path):
    payload_path2 = payload_path
    
    if os.path.basename(payload_path2) == "Payload":
        output_path = payload_path2[:len(payload_path2)-len("/Payload")]
    else:
        output_path = os.path.dirname(payload_path2)
 
    output_path = os.path.join(output_path) 
    with zipfile.ZipFile(os.path.join(output_path, "Payload.zip"), 'w', zipfile.ZIP_DEFLATED) as zip_file:  
       for root, dirs, files in os.walk(payload_path): 
           for file in files: 
               file_path = os.path.join(root, file) 
               zip_file.write(file_path, file_path.replace(payload_path, "Payload")) 
                
    clear_terminal()           
    user_new_ipa_name = input(f"enter a new name for your edited .ipa (without the .ipa at the end) \noriginal .ipa name: {file_name_no_ipa}'\n") 
    clear_terminal()
    user_new_ipa_name = user_new_ipa_name.strip() + ".ipa"
    os.rename(os.path.join(output_path, "Payload.zip"), user_new_ipa_name) 
    edited_file_path = os.path.join(output_path, user_new_ipa_name)
    os.replace(user_new_ipa_name, edited_file_path)


print("Azule: A CLI tool used to inject iOS jailbreak tweaks into jailed iOS apps.")
print("Features: \nInject debs/dylibs\nmore features will be added later")

start = input("\n\nenter 'start' to start injecting.\n")
clear_terminal()

if start.strip() == 'start':
    file_paths_input = input("Enter the path to your .deb/.dylib. (There can be several at once):\n")
    clear_terminal()
    output_dir = input("Enter an output path for your new iPA:\n")
    deb_tmp = os.path.join(output_dir, "deb_tmp")

    if not os.path.exists(deb_tmp):
        os.makedirs(deb_tmp)

    if os.name == "nt":
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

    ipa_path = input("Please enter the path to the IPA file:\n ")
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(ipa_path)
 
    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
            pl = plistlib.load(fp) 
 
    bundle_id = pl['CFBundleIdentifier'] 
    app_name = pl['CFBundleDisplayName']
    exec_name = pl['CFBundleExecutable']
    print(bundle_id,app_name, exec_name)
    
    