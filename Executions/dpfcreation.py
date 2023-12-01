import os, shutil
import subprocess
def dpfcreation(pathligand,path_receptor,dpflocation,dirmaps,cwd,nomreceptor,software):
    liganddpf = cwd+"templates/DOCKING.dpf"
    # prepare dpf4
    newcwd = cwd + "templates/"
    os.chdir(newcwd)
    print("cwd: ")
    #print(newcwd)
    print(os.getcwd())
    dpfconvert = "../parametres/prepare_dpf4.py -l "+pathligand+" -r "+path_receptor+" -o "+dpflocation 
    #print("dpf convert: ")
    #print(dpfconvert)
    os.system(dpfconvert) 
    #executabledpf = cwd + "templates/prepare_dpf4.py"
    

    #print("dpflocation: ")
    #print(dpflocation)
    # on ouvre le fichier dpf et on enlève sa premiere ligne
    with open(dpflocation, "r+") as file:
        # read a list of lines into data
        data = file.readlines()
        if software == "GPU":
            file.seek(0)
            # truncate the file
            file.truncate()
            file.writelines(data[1:])

    ligandtype = data[4][12:35]
    ligandtype = ligandtype.replace("# atoms types in ligand\n", "")
    ligandtype = ligandtype.strip()
    ligandtype = ligandtype.split(" ")

    #print("dirmaps : ")
    #print(dirmaps)
    datatoreplace = "map "+nomreceptor
    data[5] = "fld receptor_multimer.maps.fld\n"
    for x in range(len(data)):
        if data[x].find("map ", 0, 18) != -1:
            specialreplace = "map " + dirmaps +"receptor_multimer"
            #print(data[x])
            data[x] = data[x].replace(datatoreplace, specialreplace,1)
            #print(data[x])
    # print("ligand type")
    #print(ligandtype)
    # print(data)
    textfile = open(dpflocation, "w+")
    for element in data:
        textfile.write(element)
    textfile.close()
    with open(dpflocation, "r+") as file:
        # read a list of lines into data
        data = file.readlines()

        file.seek(0)
        # truncate the file
        file.truncate()
        file.writelines(data[1:])
    return ligandtype
