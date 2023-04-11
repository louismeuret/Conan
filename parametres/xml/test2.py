from lxml import etree
root = etree.Element("root")
zinc15 = etree.SubElement(root, "zinc15")
energy = etree.SubElement(zinc15, "energy")
energy = etree.Element("energy", value="7.5")
zinc16 = etree.SubElement(root, "zinc16")
energy = etree.SubElement(zinc16, "energy")
energy = etree.Element("energy", value="2")
print(etree.tostring(root, pretty_print=True))
