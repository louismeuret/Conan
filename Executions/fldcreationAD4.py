import os, shutil
import subprocess
def fldcreation(ligandtype,dirmaps,path_ligand,gridcenterx, gridcentery,gridcenterz,cwd,nomreceptor,nptsx,nptsy,nptsz,spacing, path_results):
    firstlabel = 23
    firstvariable = firstlabel + len(ligandtype) + 2

    pathreceptor = f"{path_results}/RECEPTORS/{nomreceptor}.pdbqt"

    # generer le bon fld, puis faire le docking avec autodock-gpu
    with open(cwd+"templates/good.fld", "r+") as fld:
        # read a list of lines into data

        fldcontenu = fld.readlines()


    fldcontenu[6] = "#SPACING "+spacing+"\n"
    fldcontenu[7] = "#NELEMENTS "+nptsx+" "+nptsy+" "+nptsz+"\n"
    fldcontenu[8] = "#CENTER "+gridcenterx+" "+gridcentery+" "+gridcenterz+"\n"
    fldcontenu[9] = "#MACROMOLECULE "+pathreceptor+"\n"
    fldcontenu[13] = "dim1="+str(int(nptsx)+1)+"\n"
    fldcontenu[14] = "dim2="+str(int(nptsy)+1)+"\n"
    fldcontenu[15] = "dim3="+str(int(nptsz)+1)+"\n"
    fldcontenu[17] = "veclen="+str(len(ligandtype)+2)+"\n"

    # marque les label dans le fichier fld
    for writelabel in range(len(ligandtype)):
        fldcontenu[firstlabel + writelabel] = (
            "label=" + ligandtype[writelabel] + "-affinity\n"
        )
        savelabel = writelabel + firstlabel
    fldcontenu[savelabel + 1] = "label=Electrostatics\n"
    fldcontenu[savelabel + 2] = "label=Desolvation\n"

    # marque les variables dans le fichier fld
    for writevariable in range(len(ligandtype)):
        writevariablecount = writevariable + 1
        fldcontenu[firstvariable + writevariable] = (
            "variable "
            + str(writevariablecount)
            + " file="
            + dirmaps
            + "receptor_multimer."
            + ligandtype[writevariable]
            + ".map filetype=ascii skip=6\n"
        )
        savevariable = writevariable + firstvariable
        savevariable2 = writevariable
        # print(savevariable)
    fldcoord1 = (
        "coord 1 file="
        + dirmaps
        + "receptor_multimer.maps.xyz filetype=ascii offset=0\n"
    )
    fldcoord2 = (
        "coord 2 file="
        + dirmaps
        + "receptor_multimer.maps.xyz filetype=ascii offset=2\n"
    )
    fldcoord3 = (
        "coord 3 file="
        + dirmaps
        + "receptor_multimer.maps.xyz filetype=ascii offset=4\n"
    )
    fldcontenu[20] = fldcoord1
    fldcontenu[21] = fldcoord2
    fldcontenu[22] = fldcoord3
    savevariable = savevariable + 1
    savevariable2 = savevariable2 + 2
    fldcontenu[savevariable] = (
        "variable "
        + str(savevariable2)
        + " file="
        + dirmaps
        + "receptor_multimer.e.map filetype=ascii skip=6\n"
    )
    savevariable = savevariable + 1
    savevariable2 = savevariable2 + 1
    fldcontenu[savevariable] = (
        "variable "
        + str(savevariable2)
        + " file="
        + dirmaps
        + "receptor_multimer.d.map filetype=ascii skip=6\n"
    )
    fldlocation = path_ligand + "receptor_multimer.maps.fld"
    #print(fldlocation)
    # on sauvegarde les données dans le fichier
    textfile = open(fldlocation, "w+")
    for element in fldcontenu:
        textfile.write(element)

    textfile.close()


#fldcreation("['C', 'HD', 'N', 'NA', 'OA', 'S']","/media/meuret/fbb9a6b4-8180-4f4d-83be-bbfaf21a4c32/louis/SBVS_test2/maps/cluster1frame2235_270_256_280___100_100_100","/media/gauto/fbb9a6b4-8180-4f4d-83be-bbfaf21a4c32/louis/SBVS_test2/results/DOCKED/cluster1frame2235_results__ligand1_ligand1_out","270","256","280","/media/gauto/fbb9a6b4-8180-4f4d-83be-bbfaf21a4c32/louis/SBVS_test2/","cluster1frame2235")
