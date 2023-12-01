from lxml import etree
energy={}
free_energy=[]
tree = etree.parse("DOCKING.ligand.xml")
for user in tree.xpath("/autodock_gpu/runs/run/free_NRG_binding"):
    free_energy.append(float(user.text))
    #energy[test[count]] = float(user.text) 
highest = free_energy[0]
print(highest)
x = 5
y = 9

zinc15 = etree.SubElement(root, "zinc15")
energy = etree.SubElement(zinc15, "energy")
energy.text = str(x)
zinc16 = etree.SubElement(root, "zinc16")
energy = etree.SubElement(zinc16, "energy")
energy.text = str(y)
print(etree.tostring(root, pretty_print=False))
etree.ElementTree(root).write('output.xml')
