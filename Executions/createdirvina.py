import os
import subprocess
import shutil

def create_dir(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, list_of_receptors,path_results):
    # Helper function to create a GPF file with the given template number and save it to the given path
    dir_save = []
    # Iterate over each receptor in the list of receptors
    for receptor in list_of_receptors:
        # Extract the receptor name from the receptor data
        nomreceptor = os.path.splitext(os.path.basename(receptor))[0]
        print(f"Nom receptor:{nomreceptor}")
        adressereceptor = os.path.dirname(receptor)
        print(f"Current WD = {os.getcwd()}")
        # Backup of original file, creation of folder if needed
        if not os.path.exists(f"{adressereceptor}/BAK/"):
            os.mkdir(f"{adressereceptor}/BAK/")
            
        shutil.copy(receptor,f'{adressereceptor}/BAK/{nomreceptor}_ORIGINAL.pdbqt')
        #preparereceptor = f"{cwd}parameters/prepare_receptor4.py -r {receptor} -o {receptor}"
        #os.system(preparereceptor)
        
        # Construct the save directory path
        save_dir = f'{path_results}/PARAMETERS/config_files_ligands/{nomreceptor}_{gridcenterx}_{gridcentery}_{gridcenterz}___{nptsx}_{nptsy}_{nptsz}/'
        dir_save.append(save_dir)
        # If the save directory does not exist, create it
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        

    return dir_save
