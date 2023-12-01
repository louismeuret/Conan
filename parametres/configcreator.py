from __future__ import print_function, unicode_literals
import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package]) 

with open('packages.txt') as p:
    lines = p.readlines()

for x in range(len(lines)):
    import_or_install(lines[x])

#python workflowdebug.py --useconfig yes

from PyInquirer import prompt, Separator
from pprint import pprint
import os
import shutil
from glob import glob

stringconan = '''
  sSSs    sSSs_sSSs     .S_sSSs     .S_SSSs     .S_sSSs          
 d%%SP   d%%SP~YS%%b   .SS~YS%%b   .SS~SSSSS   .SS~YS%%b         
d%S'    d%S'     `S%b  S%S   `S%b  S%S   SSSS  S%S   `S%b        
S%S     S%S       S%S  S%S    S%S  S%S    S%S  S%S    S%S        
S&S     S&S       S&S  S%S    S&S  S%S SSSS%S  S%S    S&S        
S&S     S&S       S&S  S&S    S&S  S&S  SSS%S  S&S    S&S        
S&S     S&S       S&S  S&S    S&S  S&S    S&S  S&S    S&S        
S&S     S&S       S&S  S&S    S&S  S&S    S&S  S&S    S&S        
S*b     S*b       d*S  S*S    S*S  S*S    S&S  S*S    S*S        
S*S.    S*S.     .S*S  S*S    S*S  S*S    S*S  S*S    S*S        
 SSSbs   SSSbs_sdSSS   S*S    S*S  S*S    S*S  S*S    S*S        
  YSSP    YSSP~YSSY    S*S    SSS  SSS    S*S  S*S    SSS        
                       SP                 SP   SP                
                       Y                  Y    Y                 
                                                                 
'''
stringconan2 = '''
                                :++++=:                               
                               =###**##*=                             
                              :##**+**#%%=                            
                              :**+*++++*%+                            
                              **==+++--*#%=                           
                              ##***+*+*#%%+                           
                              #%%#+++*##%%%=                          
                            .+%@%##***+*%%%#.                         
                           .+#%%%*++++=+%%%#.                         
                         .-*#%%%#*+++++*#%%%*-.                       
                      .-==++*##*=+****+++*###*+=---:                  
                    :+++===****+-=*+*=++++++++=--=+++:                
                   :**++++***++++*--**+++++++++=====++.               
                   -***###**++++=+--+**+++++++**##*++*=               
                   =*+=+###**+===+*+##**+==+++*#%#==+**=.             
                 .+*#++*%%%##*+==**##%#*+=+**#%%%%*++****.            
                 =##*+*###%%%%%###***##*##%%%%%##**#***##=            
                 *##**#: +%%%%%##*******##**##%#+  =*###**.           
                -***##.   =%%%%##*+***++***####:     -%#**+           
                +#**#*    .###%%##**#***###*##=      :#*+**           
                :##***-   :##*###*+***+**#***#:      ##*+*-           
                 =+++**+= +##**###******#****#      .%%%*+ 
'''
print(stringconan2)
print("Welcome to...")

print(stringconan)
#databases = ['obabel','Auto3d']
goodfoldersnames = []
def software_prompt():
    software_prompt = {
        'type': 'list',
        'name': 'software',
        'message': 'What do you want to do with Conan ?',
        'choices': ['Virtual Screening', 'Post Process (not working yet)', 'See Results (not working yet)','just execute it'],
            }
    answers = prompt(software_prompt)
    return answers['software']


software = software_prompt()

f = open("databases.txt", "r")
dbstore = f.readline()
dbstore = dbstore.replace("\n","")
#print(dbstore)
toscan = dbstore + "/*/"
#print(toscan)
databases = glob(toscan)
databases.append("Change the directory of Databases")
#print(databases)


questions = [
{  
        'type': 'list',
        'name': 'software1',
        'message': 'What software do you want to dock with ?',
        'choices': ['Autodock Vina', 'Autodock GPU', 'Gnina'],
    },

    {
        'type': 'list',
        'name': 'database',
        'message': 'What database do you want to use ?',
        'choices': databases,
    },

]
questiondb = [
            {
        'type': 'input',
        'name': 'newdatabase',
        'message': 'Enter the new path for the databases (/path/to/dbs)',
     },
            ]

questions6 = [
{  
        'type': 'list',
        'name': 'launch',
        'message': 'Do you want to execute Conan now ?',
        'choices': ['yes', 'no'],
    },
]

if software == 'Virtual Screening':
    f = open("databases.txt", "r")
    dbstore = f.readline()
    dbstore = dbstore.replace("\n","")
    #print(dbstore)
    toscan = dbstore + "/*/"
    #print(toscan)
    databases = glob(toscan)
    databases.append("Change the directory of Databases")
    #print(databases)
    #print("Current folder for databases: "+dbstore)
    answers = prompt(questions)
    toscan1 = answers['database']+"/*/"
    dbscan = glob(toscan1)
    goodfolders = []
    for x in range(len(dbscan)):
        #print(dbscan[x])
        toscan2 = dbscan[x]+"/**/*.pdbqt"
        for f in glob(toscan2, recursive=False):
            #print(f)
            goodfolders.append(dbscan[x])
            goodfoldersnames.append(dbscan[x].split("/")[-2])
            break
    if (answers['database'] == "Change the directory of Databases"):
        newdb = prompt(questiondb)
        dbfile = open("databases.txt", "w")

        dbfile.write(newdb['newdatabase'])
        dbfile.close()
        answers = prompt(questions)
    
    #print(goodfoldersnames)
    #print(goodfolders)


    #pprint(answers)


#print(answers['database'])

questions2 = [
        {
        'type': 'list',    
        'name': 'database2',
        'message': 'I found pdbqts in theses folders, which one do you want to use ?',
        'choices': goodfoldersnames,
    },

    {
        'type': 'input',
        'name': 'threads',
        'message': 'How many process shoud run at the same time ?',
     },
        {
        'type': 'input',
        'name': 'nruns',
        'message': 'How many runs should the docking program take at maximum ?',
     },
    {  
        'type': 'list',
        'name': 'debug',
        'message': 'Do you need debug mode activated ?',
        'choices': ['yes', 'no'],
    },


]
question4 = [
    {  
        'type': 'list',
        'name': 'receptors',
        'message': 'Are theses good to you ? you can also directly move them into the receptors folder',
        'choices': ['yes its good', 'no i need to change them'],
    },

        ]
question5 = [
    {   
        'type': 'input',
        'name': 'pathreceptors',
        'message': 'Input here the folder where the receptors are, they will be cleaned with the preparereceptor script, and then added to the destination folder.',
    },

        ]
questions3 = [
     #Separator('= Center of the box ='),
         {
        'type': 'input',
        'name': 'centerx',
        'message': 'X center of the box',
     },
    {
        'type': 'input',
        'name': 'centery',
        'message': 'Y center of the box',
     },
    {
        'type': 'input',
        'name': 'centerz',
        'message': 'Z center of the box',
     },
    #Separator('= Dimensions of the box ='),
    {  
        'type': 'input',
        'name': 'sizex',
        'message': 'X dimension of the box',                          
     },
        {  
        'type': 'input',
        'name': 'sizey',
        'message': 'Y dimension of the box',                          
     },
        {  
        'type': 'input',
        'name': 'sizez',
        'message': 'Z dimension of the box',                          
     },
        {  
        'type': 'input',
        'name': 'spacing',
        'message': 'Spacing for Autodock GPU (it will be converted for autodock-Vina, default 0.365',                          
     },

        ]
def launchconan():
    os.chdir("../Executions")
    print(os.getcwd())
    os.system("python ../Executions/workflowdebug.py --useconfig yes")

def preparereceptors(path):
    toscan4 = path + "/*.pdbqt"
    receptors = glob(toscan4)
    for x in range(len(receptors)):
        namereceptor = receptors[x].split("/")[-1].replace(".pdbqt","")
        pathreceptor = "../receptors/"+namereceptor+".pdbqt"
        print(pathreceptor)
        pdbqtconvert = "./prepare_receptor4.py -r "+receptors[x]+" -o "+pathreceptor
        os.system(pdbqtconvert)




if software == 'Virtual Screening':
    answers2 = prompt(questions2)
    toscan3 = "../receptors/*.pdbqt"
    receptorlist = glob(toscan3)
    stringreceptors = ""
    for x in range(len(receptorlist)):
        stringreceptors = stringreceptors + receptorlist[x] + "\n"
    
    if (len(receptorlist)>0):
        print("found theses receptors in the receptors directory : \n" + stringreceptors)
        answerreceptors = prompt(question4)
        if answerreceptors['receptors'] == "no i need to change them":
            pathreceptors = prompt(question5)
            preparereceptors(pathreceptors['pathreceptors'])

    if (len(receptorlist)==0):
        print("No receptors found in the receptors directory")
        pathreceptors = prompt(question5)
        preparereceptors(pathreceptors['pathreceptors'])


        
    
    print("final configuration")
    answersparameters = prompt(questions3)

    f = open("conanconfig.txt","w+")
    if answers['software1'] == 'Autodock Vina':
        docksoft = "vina"
    elif answers['software1'] == 'Autodock GPU':
        docksoft = "gpu"
    elif answers['software1'] == 'Gnina':
        docksoft = "gnina"
    
    f.write("#SOFTWARE# "+docksoft+" \n")
    f.write("#DEBUG# "+answers2['debug']+" \n")
    f.write("#THREADS# "+str(answers2['threads'])+" \n")
    f.write("#NRUNS# "+str(answers2['nruns'])+" \n")
    f.write("#PATHDB# "+answers['database']+answers2['database2']+" \n")
    f.write("#SPACING# "+str(answersparameters['spacing'])+" \n")
    f.write("#CENTERX# "+str(answersparameters['centerx'])+" \n")
    f.write("#CENTERY# "+str(answersparameters['centery'])+" \n")
    f.write("#CENTERZ# "+str(answersparameters['centerz'])+" \n")
    f.write("#SIZEX# "+str(answersparameters['sizex'])+" \n")
    f.write("#SIZEY# "+str(answersparameters['sizey'])+" \n")
    f.write("#SIZEZ# "+str(answersparameters['sizez'])+" \n")
    f.close()

    launch = prompt(questions6)
    if launch['launch'] == 'yes':
        print("Config file created")
        print("Executed Conan...")
        launchconan()
    if launch['launch'] == 'no':
        print("Config file created")
        print("Exiting...")
        
if software == 'just execute it':
    launchconan()



