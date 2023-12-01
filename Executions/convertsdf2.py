import os
import subprocess
def convertsdf(ligandfiletotal,ligandfilename,pathdb,cwd):
    name_file = ligandfiletotal[:-4]+".pdb"
    obabel_conv = f"obabel -isdf {ligandfiletotal} -o pdb -O {name_file}"
    os.system(obabel_conv)
    pdbqtlocation = pathdb + ligandfilename + ".pdbqt"
    if os.path.exists(pdbqtlocation) is False:
        pdblocation = name_file 
        print(f"PDB: {pdblocation}")
    #print("pdb:")
    #print(pdblocation)
        ligandfiletotal = pathdb + ligandfilename + ".pdbqt"
        newdir = cwd + "/parametres/prepare_ligand4.py"
        lncommand = "ln -s "+newdir+ " "+pathdb


        try:
        #if os.path.isfile(newdir):
                #print("file already exist")
            #else:
            print ("File not exist")
            os.system(lncommand)
        except:
            pass
        cwddir = cwd + "parametres/"
        os.chdir(pathdb)    
    #print("-------------%s"%pdblocation)
    #print("------------%s---------------"%cwddir)
        print(f"PDBQT: {ligandfiletotal}")
        pdbqtconvert = "./prepare_ligand4.py -l "+pdblocation+" -o "+ligandfiletotal
    
        os.system(pdbqtconvert)
    #os.system("./prepare_ligand4.py -l ligand1_out.pdb -o ligand1_out.pdbqt")
    #print("done convert")
        os.chdir(cwd)
    else:
        ligandfiletotal = pdbqtlocation

    return ligandfiletotal


#convertsdf("/media/meuret/fbb9a6b4-8180-4f4d-83be-bbfaf21a4c32/louis/TESTS/DESCRIPTORS/results/_ligand1/ligand1_out.sdf","ligand1_out","/media/meuret/fbb9a6b4-8180-4f4d-83be-bbfaf21a4c32/louis/TESTS/DESCRIPTORS/results/_ligand1/","/media/meuret/fbb9a6b4-8180-4f4d-83be-bbfaf21a4c32/louis/SBVS_test2/")
