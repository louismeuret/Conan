import os
import time
def createconf(nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz,spacing,path_receptor,receptorname,results_path):
    vinax = nptsx
    vinay = nptsy
    vinaz = nptsz
    filecontent = "receptor = "+path_receptor+"\n"+"\n"
    filecontent = filecontent + "center_x = "+gridcenterx+"\n"
    filecontent = filecontent + "center_y = "+gridcentery+"\n"
    filecontent = filecontent + "center_z = "+gridcenterz+"\n"+"\n"

    filecontent = filecontent + "size_x = "+vinax+"\n"
    filecontent = filecontent + "size_y = "+vinay+"\n"  
    filecontent = filecontent + "size_z = "+vinaz+"\n"+"\n"

    filecontent = filecontent + "num_modes=9"+"\n"+"\n"

    filecontent = filecontent + "cpu = 1"+"\n"+"\n"

    filecontent = filecontent + "energy_range = 4"+"\n"
    savedir = f"{results_path}/PARAMETERS/config_files_ligands/{receptorname}_{gridcenterx}_{gridcentery}_{gridcenterz}___{nptsx}_{nptsy}_{nptsz}/{receptorname}.txt"
    # first create the path
    os.makedirs(os.path.dirname(savedir), exist_ok=True)
    # then save the file
    with open(savedir, 'w+') as f:
        f.write(filecontent)
    f.close()
