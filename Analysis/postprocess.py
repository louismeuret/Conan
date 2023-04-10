import os
import shutil
cwd = os.getcwd()

cwd = cwd.replace("Analysis","")

subfolders = [ f.path for f in os.scandir(cwd+"results/DOCKED/") if f.is_dir() ]
from os.path import exists
from lxml import etree
root = etree.Element("root")
import centremasse as centre
meilleureenergie = 0
numberofsuccess = 0
numberofechec = 0
meilleurligand = ""

for x in range(len(subfolders)):
        #try:
        zincpdb = subfolders[x]+"/best.pdbqt"
        if os.path.exists(zincpdb) == True:
            
            with open(zincpdb, "r+") as file:
            # read a list of lines into data
                data = file.readlines()
            namezinc = data[0]
            namezinc = namezinc.replace("REMARK  Name = ", "")
            namezinc = namezinc.strip()    
            #print(namezinc)
            free_energy = []
            os.chdir(subfolders[x])
            toparse = namezinc + ".xml"
            bestligandpaste = cwd+"results/BEST/" + namezinc + ".pdbqt"
            shutil.copyfile(zincpdb, bestligandpaste)
            print(toparse)
            tree = etree.parse(toparse)
            for user in tree.xpath("/autodock_gpu/runs/run/free_NRG_binding"):
                free_energy.append(float(user.text))
                # energy[test[count]] = float(user.text)
            highest = free_energy[0]
            #print(free_energy)
            #print(highest)
            if highest < meilleureenergie:
                meilleureenergie = highest
                meilleurligand = namezinc
            storenamezinc = namezinc
            namezinc = etree.SubElement(root, namezinc)
            energy = etree.SubElement(namezinc, "energy")
            energy.text = str(highest)

            centrex, centrey,centrez = centre.centremasse(zincpdb)
            nomligand = etree.SubElement(namezinc, "nomligand")
            nomligand.text = str(storenamezinc)
            bestcentrex = etree.SubElement(namezinc, "coordx")
            bestcentrex.text = str(centrex)
            bestcentrey = etree.SubElement(namezinc, "coordy")
            bestcentrey.text = str(centrey)
            bestcentrez = etree.SubElement(namezinc, "coordz")
            bestcentrez.text = str(centrez)
            numberofsuccess = numberofsuccess + 1

        else:
            print("error")
            numberofechec = numberofechec + 1
print("meilleur energie:")
print(meilleureenergie)
print("de: ")
print(meilleurligand)
print("succès: ")
print(numberofsuccess)
print("echcecs: ")
print(numberofechec)
etree.tostring(root, pretty_print=True)
namexml = cwd + "results/XML/output"+str(len(subfolders))+".xml"
etree.ElementTree(root).write(namexml)
        #except:
            #pass
            #print("error")
