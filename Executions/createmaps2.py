import os
import subprocess
import shutil

def create_maps(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, list_of_receptors):
    # Helper function to create a GPF file with the given template number and save it to the given path
    dir_save = []
    def make_gpf_file(template_number, save_path,nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz,spacing,adressereceptor,nomreceptor):
        # Open the template file for reading

        with open(f'{cwd}templates/GPF/DOCKING{template_number}.gpf', 'r') as template_file:
            # Read all lines from the template file
            data = template_file.readlines()

        # Replace placeholders in the template with the specified values
        data[0] = f'npts {nptsx} {nptsy} {nptsz}\n'
        data[2] = f'spacing {spacing}\n'
        data[5] = f'receptor {adressereceptor}{nomreceptor}.pdbqt\n'
        data[6] = f'gridcenter {gridcenterx} {gridcentery} {gridcenterz}\n'

        # Open the save file for writing
        with open(save_path, 'w') as save_file:
            # Write the modified data to the save file
            save_file.writelines(data)

    # Helper function to create a symlink in the target directory with the given name
    def make_symlink(target_dir, link_name):
        try:
            # Create the symlink
            os.symlink(f'{cwd}parametres/', link_name)
        except OSError:
            # If the symlink already exists, do nothing
            pass

    # Helper function to remove the specified file
    def remove_fld_file(fld_path):
        try:
            # Remove the file
            os.remove(fld_path)
        except OSError:
            # If the file does not exist, do nothing
            pass
    
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
        save_dir = f'{cwd}maps/{nomreceptor}_{gridcenterx}_{gridcentery}_{gridcenterz}___{nptsx}_{nptsy}_{nptsz}/'
        dir_save.append(save_dir)
        # If the save directory does not exist, create it
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
# Create three GPF files using the templates and save them to the save directory
            for i in range(1, 4):
                make_gpf_file(i, f'{save_dir}DOCKING{i}.gpf',nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz,spacing,adressereceptor,nomreceptor)
            make_symlink(cwd, save_dir)
            os.chdir(save_dir)
            for i in range(1, 4):
                os.chdir(save_dir)
                if shutil.which("autogrid4") != "":
                    os.system(f'autogrid4 -p {save_dir}DOCKING{i}.gpf')
                else:
                    pathautogrid = f"{cwd}parametres/executables/autogrid4" 
                    os.system(f"{pathautogrid} -p {save_dir}DOCKING{i}.gpf")
                os.chdir(cwd+"Executions") 
                #subprocess.run(f'autogrid4 -p {save_dir}DOCKING{i}.gpf')
        remove_fld_file(f'{save_dir}receptor_multimer.maps.fld')

    return dir_save
