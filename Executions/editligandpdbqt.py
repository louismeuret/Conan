import os, shutil
import subprocess
def editligandpdbqt(software,currentligand, receptorname, dossiertemps, ligandfilename, cwd, ligandfirstpath,path_results):
    ligandpdb = currentligand
    nameligand = ligandfilename
    #print("nameligand: ")
    #print(ligandfilename)
    #print("ligandfirstpath: ")
    #print(ligandfirstpath)
    #path_ligand1 = cwd + "results_"+software+"/DOCKED/"+ligandfirstpath+"/"
    path_ligand =f"{path_results}/DOCKED/{ligandfirstpath}/{receptorname}_{os.path.splitext(os.path.basename(ligandfilename))[0]}_{dossiertemps}/"
    #print(path_ligand1)
    if not os.path.exists(path_ligand):
        os.makedirs(path_ligand)
        #print("Directory " , path_ligand1 ,  " Created ")
    else:
        #print("echec")
        pass
    liganddirpaste = path_ligand + nameligand 

    #os.system('ln -sf %s %s'%(ligandpdb,path_ligand))
    os.symlink('%s'%ligandpdb, '%s'%liganddirpaste)
    return path_ligand, liganddirpaste, nameligand
