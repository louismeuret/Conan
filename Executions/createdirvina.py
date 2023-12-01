import os
import subprocess
import shutil

def create_dir(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, list_of_receptors):
    # Helper function to create a GPF file with the given template number and save it to the given path
    dir_save = []
    # Iterate over each receptor in the list of receptors
    for receptor in list_of_receptors:
        # Extract the receptor name from the receptor data
        list_of_receptorstemp = receptor[13:]
        nomreceptor = list_of_receptorstemp[:-6]
        adressereceptor = cwd+"receptors/"
        print(f"Current WD = {os.getcwd()}")
        # Backup of original file, creation of folder if needed
        if not os.path.exists(f"{adressereceptor}/BAK/"):
            os.mkdir(f"{adressereceptor}/BAK/")
            
        shutil.copy(receptor,f'{adressereceptor}/BAK/{nomreceptor}_ORIGINAL.pdbqt')
        preparereceptor = f"{cwd}parametres/prepare_receptor4.py -r {receptor} -o {receptor}"
        os.system(preparereceptor)
        
        # Construct the save directory path
        save_dir = f'{cwd}parametres/temp_files/{nomreceptor}_{gridcenterx}_{gridcentery}_{gridcenterz}___{nptsx}_{nptsy}_{nptsz}/'
        dir_save.append(save_dir)
        # If the save directory does not exist, create it
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
# Create three GPF files using the templates and save them to the save directory

    return dir_save
