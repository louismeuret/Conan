from rdkit.Chem import Descriptors
from rdkit import Chem
file_names = "/home/louis/SBVS/Analysis/smartp/test2.mol"
m = Chem.MolFromMolFile("/home/louis/SBVS/Analysis/smartp/test.sdf")
print(m)
print(Chem.Crippen.MolLogP(m))