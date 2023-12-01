import os, shutil
import subprocess
def createmaps(receptorname,adressereceptor,nomreceptor,nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz,spacing,cwd,listofreceptors):
    nptsx = nptsx
    nptsy = nptsy
    nptsz = nptsz

    gridcenterx = gridcenterx
    gridcentery = gridcentery
    gridcenterz = gridcenterz

    spacing = spacing
    for receptors in listofreceptors:
        listofreceptorstemp = listofreceptors[receptors][13:]
        nomreceptor = listofreceptorstemp[:-6]
        receptorname = nomreceptor
        adressereceptor = cwd+"receptors/"
        createdirgpf = (
            cwd
            + "maps/"
            + receptorname
            + "_"
            + gridcenterx
            + "_"
            + gridcentery
            + "_"
            + gridcenterz
            + "___"
            + nptsx
            + "_"
            + nptsy
            + "_"
            + nptsz
            + "/"
        )
        dirmaps = createdirgpf

        if not os.path.exists(createdirgpf):
            os.mkdir(createdirgpf)
            # print("Directory " , createdirgpf ,  " Created ")
            for x in range(1, 4):
                adresseGPF = cwd+"templates/GPF/DOCKING" + str(x) + ".gpf"
                with open(adresseGPF, "r+") as file:
                    # read a list of lines into data
                    data = file.readlines()
                data[0] = "npts " + nptsx + " " + nptsy + " " + nptsz + "\n"
                data[2] = "spacing" + spacing + "\n"
                data[5] = "receptor " + adressereceptor + nomreceptor + ".pdbqt\n"
                data[6] = (
                    "gridcenter "
                    + gridcenterx
                    + " "
                    + gridcentery
                    + " "
                    + gridcenterz
                    + "\n"
                )
                savegpf = dirmaps + "DOCKING" + str(x) + ".gpf"
                textfile = open(savegpf, "w+")
                for element in data:

                    textfile.write(element)

                textfile.close()
            try:
                os.symlink(cwd+"parametres/", dirmaps)
            except OSError:
                pass
            os.chdir(dirmaps)
            for x in range(1, 4):
                opengpf = dirmaps + "DOCKING" + str(x) + ".gpf"
                autogrid = "autogrid4 -p " + opengpf
                os.system(autogrid)
        else:
            #print("")
            pass
        removefld = dirmaps + "receptor_multimer.maps.fld"
        try:
            os.remove(removefld)
        except OSError:
            pass

    return dirmaps
