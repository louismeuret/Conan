import postprocess as pp
from tabulate import tabulate

sortabc,sortnrj = pp.process_results("/home/louis/Téléchargements/PROJETISDD/results_VINA","VINA")
print(tabulate(sortabc))
print(tabulate(sortnrj))
