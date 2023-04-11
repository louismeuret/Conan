def findpdbqt(countligand, pathdb):
    ligandfilename = "outputfile" + str(countligand)
    ligandfiletotal = pathdb + ligandfilename + ".pdbqt"
    #print("ligandfiletotal: ")
    #print(ligandfiletotal)
    return ligandfiletotal, ligandfilename
