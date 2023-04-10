def obabelunpack(dbused):
    # print(pathdb)
    os.chdir(pathdb)
    file = ligandslices[0] + ligandslices[1] + ".xaa.pdbqt"
    # print(file)
    obabel = "obabel -ipdbqt " + file + " -opdbqt -O ligand.pdbqt -m"
    os.system(obabel)
    os.remove(file)
