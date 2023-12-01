import os
import time
def createconf(nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz,spacing,path_receptor,receptorname):
    import time
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
    savedir = "parametres/temp_files/"+receptorname+"_"+gridcenterx+"_"+gridcentery+"_"+gridcenterz+"___"+nptsx+"_"+nptsy+"_"+nptsz+"/"+receptorname+".txt"
    #print(os.getcwd())
    f = open(savedir, 'w+')
    f.write(filecontent)
    f.close()
