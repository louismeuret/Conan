from pymol import cmd
import pymol
import sys

# Accédez aux valeurs des arguments comme suit :
print(sys.argv[1])
print(sys.argv[2])
print("launchpymol here")
pymol.finish_launching()
cmd.load(str(sys.argv[1]))
cmd.load(str(sys.argv[2]))
cmd.zoom()

