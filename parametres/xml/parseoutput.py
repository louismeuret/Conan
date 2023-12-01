from lxml import etree

root = etree.parse("output.xml")
good = []
#print(root)
for x in range(2,1500):
    name = "outputfile"+str(x)
    #try:
    for a in root.findall(name):
        value = float(a.find('energy').text)
        if value < -8:
            good.append(float(a.find('energy').text))
            print
    #except:
        #print(name)
        #pass

print(good)
