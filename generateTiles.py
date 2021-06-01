import sys
import os
import math
import shutil
from PIL import Image

print("Journeymap to Coordman tiles converter")
print("Note: This program may take a while to run")
print("Please insert the full path to your Journeymap images folder (eg C:\\Users\\Popstonia\\AppData\\Roaming\\.minecraft\\journeymap\\data\\mp\\2b2t\\):")
jmpath = input()
levelcount = 16

def generateMap(source,destination,dimension):
    os.mkdir(destination[:-2])
    os.mkdir(destination)

    jmdirs = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","night","day"]
    if not dimension == "DIM0":
        jmdirs.reverse()
    for jmdir in jmdirs:
        print(f"Copying files... ({jmdirs.index(jmdir)+1}/{len(jmdirs)})")
        jmpath = f"{source}/{jmdir}/"
        jmdest = f"{destination}/"
        if not os.path.isdir(jmpath):
            continue
        jmfiles = os.listdir(jmpath)
        i = 0
        for file in jmfiles:
            i+=1
            if i % 100 == 0:
                print(f"Copying files... ({jmdirs.index(jmdir)}/{len(jmdirs)}) - {math.floor(10000*i/len(jmfiles))/100}% ({i}/{len(jmfiles)})")
            if os.path.exists(f"{jmdest}/{file}"):
                try:
                    srcim = Image.open(f"{jmpath}/{file}")
                    destim = Image.open(f"{jmdest}/{file}")
                    destim.paste(srcim, (0, 0), srcim)
                    destim.save(f"{jmdest}/{file}")
                except:
                    print(f"File {jmpath}/{file} and/or {jmdest}/{file} is corrupted!")
            else:
                shutil.copyfile(f"{jmpath}/{file}",f"{jmdest}/{file}")

def generateZooms(folder,level):
    """ Generate zoom 'level' PNGs based on a one unit smaller level """
    os.mkdir(f"{folder}/" + level)
    prevfolder = f"{folder}/" + str(int(level)+1)
    toProcess = os.listdir(prevfolder)
    toProcessLen = len(toProcess)

    while len(toProcess) > 0:
        print(f"Generating level {level.replace('-','')}/{levelcount}: {math.floor(10000*(toProcessLen-len(toProcess))/toProcessLen)/100}% done ({toProcessLen-len(toProcess)}/{toProcessLen})")
        currentpic = toProcess[0]
        coords = [math.floor(int(currentpic.split(",")[0])/2),math.floor(int(currentpic.split(",")[1].split(".")[0])/2)]
        newpic = Image.new('RGBA', (1024, 1024))
        for x in range(2):
            for z in range(2):
                try:
                    nextpic = f"{coords[0]*2 + x},{coords[1]*2 + z}.png"
                    toProcess.remove(nextpic)
                except ValueError:
                    continue # File doesn't exist - ignore and continue
                newpic.paste(Image.open(prevfolder + "/" + nextpic), (x*512,z*512))
        newpic = newpic.resize((512,512))
        newpic.save(f"{folder}/{level}/{coords[0]},{coords[1]}.png")

# Delete tiles folder
if os.path.isdir("tiles/"):
    shutil.rmtree("tiles/")
os.mkdir("tiles")

for dimension in ["DIM-1","DIM0","DIM1"]:
    print(f"Copying files... ({dimension})")
    generateMap(f"{jmpath}/{dimension}",f"tiles/{dimension}/0",dimension)

    print("Generating zoom levels...")
    for level in range(levelcount):
        generateZooms(f"tiles/{dimension}","-" + str(level + 1))