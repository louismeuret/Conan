import os
import subprocess
import shutil
import logging

def create_maps(nptsx, nptsy, nptsz, gridcenterx, gridcentery, gridcenterz, spacing, cwd, list_of_receptors,path_results):
    logging.basicConfig(filename=f'{path_results}/FILES/createmaps.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    try:
        logging.debug("Creating maps")
        dir_save = []
        def make_gpf_file(template_number, save_path,nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz,spacing,adressereceptor,nomreceptor):
            with open(f'{cwd}templates/GPF/DOCKING{template_number}.gpf', 'r') as template_file:
                data = template_file.readlines()
            data[0] = f'npts {nptsx} {nptsy} {nptsz}\n'
            data[2] = f'spacing {spacing}\n'
            data[5] = f'receptor {adressereceptor}/{nomreceptor}.pdbqt\n'
            data[6] = f'gridcenter {gridcenterx} {gridcentery} {gridcenterz}\n'
            with open(save_path, 'w') as save_file:
                save_file.writelines(data)
        def make_symlink(target_dir, link_name):
            try:
                os.symlink(f'{cwd}parameters/', link_name)
            except FileExistsError:
                pass
        def remove_fld_file(fld_path):
            try:
                os.remove(fld_path)
            except FileNotFoundError:
                pass
        for receptor in list_of_receptors:
            nomreceptor = os.path.splitext(os.path.basename(receptor))[0]
            logging.debug(f"Nom receptor:{nomreceptor}")
            adressereceptor = os.path.dirname(receptor)
            logging.debug(f"Adresse:{adressereceptor}")
            logging.debug(f"Current WD = {os.getcwd()}")
            if not os.path.exists(f"{adressereceptor}/BAK/"):
                os.makedirs(f"{adressereceptor}/BAK/")    
            shutil.copy(receptor,f'{adressereceptor}/BAK/{nomreceptor}_ORIGINAL.pdbqt')
            save_dir = f'{path_results}/MAPS/{nomreceptor}_{gridcenterx}_{gridcentery}_{gridcenterz}___{nptsx}_{nptsy}_{nptsz}/'
            dir_save.append(save_dir)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                for i in range(1, 4):
                    make_gpf_file(i, f'{save_dir}DOCKING{i}.gpf',nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz,spacing,adressereceptor,nomreceptor)
                make_symlink(cwd, save_dir)
                os.chdir(save_dir)
                for i in range(1, 4):
                    os.chdir(save_dir)
                    if shutil.which("autogrid4") != "":
                        os.system(f'autogrid4 -p {save_dir}DOCKING{i}.gpf')
                    else:
                        pathautogrid = f"{cwd}parameters/executables/autogrid4" 
                        os.system(f"{pathautogrid} -p {save_dir}DOCKING{i}.gpf")
                    os.chdir(cwd+"Executions") 
            remove_fld_file(f'{save_dir}receptor_multimer.maps.fld')
        return dir_save
    except Exception as e:
        logging.error(f"An error occurred while creating maps: {e}")
        raise
