from pymol import cmd
import pymol
import sys
import os
def viewreceptor(pathrecs,nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz):
    pymol.finish_launching()
    for path in pathrecs:
        print(path)
        cmd.load(path)
    cmd.run("gridbox.py")
    cmd.do(f"gridbox {gridcenterx},{gridcentery},{gridcenterz},{nptsx},{nptsy},{nptsz},trasp=0.5")
    cmd.turn('x',45)
    cmd.turn('y',45)
    cmd.turn('z',45)
    cmd.zoom()
    cmd.refresh()

nptsx = float(sys.argv[1])
nptsy = float(sys.argv[2])
nptsz = float(sys.argv[3])
gridcenterx = float(sys.argv[4])
gridcentery = float(sys.argv[5])
gridcenterz = float(sys.argv[6])
os.chdir("../parametres")
with open("temp_files/pathreceptors.txt") as file:
    listofreceptors = [line.rstrip() for line in file]
print(listofreceptors)
viewreceptor(listofreceptors,nptsx,nptsy,nptsz,gridcenterx,gridcentery,gridcenterz)
