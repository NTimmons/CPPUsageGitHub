import glob, os
from collections import Counter
import sys
import urllib.request
import json
import win32api, win32con
from shutil import copyfile



cpp_11_lib = []
with open('cpp_11_lib.csv', 'r') as csvfile:
    cpp_11_lib = csvfile.read().splitlines()
cpp_11_libUsed = Counter()
cpp_11_libUsedTotal = Counter()
for e in cpp_11_lib:
    cpp_11_libUsed[e] = 0
    cpp_11_libUsedTotal[e] = 0

cpp_14_lib = []
with open('cpp_14_lib.csv', 'r') as csvfile:
    cpp_14_lib =csvfile.read().splitlines()
cpp_14_libUsed = Counter()
cpp_14_libUsedTotal = Counter()
for e in cpp_14_lib:
    cpp_14_libUsed[e] = 0
    cpp_14_libUsedTotal[e] = 0

cpp_17_lib = []
with open('cpp_17_lib.csv', 'r') as csvfile:
    cpp_17_lib = csvfile.read().splitlines()
cpp_17_libUsed = Counter()
cpp_17_libUsedTotal = Counter()
for e in cpp_17_lib:
    cpp_17_libUsed[e] = 0
    cpp_17_libUsedTotal[e] = 0

dir = "./"
pages = 5
for x in range(1, pages+1):
    githubJSON = 0
    with urllib.request.urlopen('https://api.github.com/search/repositories?q=language:cpp&sort=stars&order=desc&per_page=100&page='+str(x) ) as response:
       githubJSON = response.read()

    githubProjectlist   = json.loads(githubJSON)
    printableDir        = dir.replace('\\', '_')
    printableDir        = printableDir.replace(':', '_')

    for gitProj in githubProjectlist['items']:
        projName = gitProj['name']
        gitURL   = gitProj['html_url']
        clone       =   "git clone " + gitURL
        os.system(clone) # Cloning

        addedTo11= False
        addedTo14= False
        addedTo17= False

        types = ('.h', '.cpp', '.cc', '.hpp')
        for t in types:
            filelist = glob.glob(dir+"/"+projName+"/**/*" + t, recursive=True)
            filecount = len(filelist)
            counter = 0;

            if filecount != 0:
                print(projName + ": Percentage of " + t + " is " + str((counter/filecount)*100.0) + ".")

            for file in filelist:
                try:
                    line = open(file, encoding="ascii", errors="surrogateescape").read()
                    usingStd = line.find("using namespace std;")

                    for entry in cpp_11_lib:
                        index = line.find(entry+'(')
                        if index == -1:
                            index = line.find(entry+'<')
                        if index == -1 and usingStd != -1:
                            index = line.find(entry[5:])
                        if index != -1:
                            if addedTo11 == False:
                                cpp_11_libUsedTotal[entry]  += 1;
                                addedTo11 = True
                            cpp_11_libUsed[entry]       = 1;

                    for entry in cpp_14_lib:
                        index = line.find(entry+'(')
                        if index == -1:
                            index = line.find(entry+'<')
                        if index == -1 and usingStd != -1:
                            index = line.find(entry[5:])
                        if index != -1 :
                            if addedTo14 == False:
                                cpp_14_libUsedTotal[entry]  += 1;
                                addedTo14 = True
                            cpp_14_libUsed[entry]       = 1;

                    for entry in cpp_17_lib:
                        index = line.find(entry+'(')
                        if index == -1:
                            index = line.find(entry+'<')                
                        if index == -1 and usingStd != -1:
                            index = line.find(entry[5:])
                        if index != -1:
                            if addedTo17 == False:
                                cpp_17_libUsedTotal[entry]  += 1;
                                addedTo17 = True
                            cpp_17_libUsed[entry]       = 1;


                except ValueError:
                    print ("error reading file: " + file)


                counter += 1
                update = (counter % 100) == 1
                if update:
                    print(projName + ": Percentage of " + t + " is " + str((counter/filecount)*100.0) + ".")


        # rm the projectdir
        rmDir = "rmdir " + projName + " /s /q"
        #os.system(rmDir) # Cloning

        with open(projName+"_Output_Single.csv", 'w+') as f:
            f.write("--Output for:" + projName)
            f.write("--C++11 Usage--\n")
            for k,v in  sorted(cpp_11_libUsed.most_common()):
                f.write( "{}, {}\n".format(k,v) )
            f.write("--C++14 Usage--\n")
            for k,v in  sorted(cpp_14_libUsed.most_common()):
                f.write( "{}, {}\n".format(k,v) )
            f.write("--C++17 Usage--\n")
            for k,v in  sorted(cpp_17_libUsed.most_common()):
                f.write( "{}, {}\n".format(k,v) )

        cpp_11_libUsed = Counter()
        cpp_14_libUsed = Counter()
        cpp_17_libUsed = Counter()

        with open("Total"+"_Output.csv", 'w+') as f:
            f.write("--C++11 Usage--\n")
            for k,v in  sorted(cpp_11_libUsedTotal.most_common()):
                f.write( "{}, {}\n".format(k,v) )
            f.write("--C++14 Usage--\n")
            for k,v in  sorted(cpp_14_libUsedTotal.most_common()):
                f.write( "{}, {}\n".format(k,v) )
            f.write("--C++17 Usage--\n")
            for k,v in  sorted(cpp_17_libUsedTotal.most_common()):
                f.write( "{}, {}\n".format(k,v) )

        copyfile("Total"+"_Output.csv", "Total"+"_Output.csv.backup")

