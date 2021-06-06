#!/usr/bin/env python3

"""
Copy all journeymap files to new location and generate different zoom levels
"""

import math
import multiprocessing as mp
import os
import re
import shutil

from PIL import Image
from tqdm import tqdm

levelcount = 16
printfreq = 100
mp_cores = mp.cpu_count() - 1
dimensions = ["DIM-1", "DIM0", "DIM1"]


def generateMap(source, destination, dimension):
    """ Generates base level by merging all journeymap layers over eachother """
    os.mkdir(destination[:-2])
    os.mkdir(destination)

    jmdirs = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "night", "day"]
    if not dimension == "DIM0":
        jmdirs.reverse()
    for jmdir in jmdirs:
        print(f"Copying files... ({jmdirs.index(jmdir) + 1}/{len(jmdirs)})")
        jmpath = f"{source}/{jmdir}/"
        jmdest = f"{destination}/"
        if not os.path.isdir(jmpath):
            continue
        jmfiles = os.listdir(jmpath)
        if __name__ == '__main__':
            with mp.Pool(mp_cores) as p:
                for _ in tqdm(p.imap(mergeLayers, [(file, jmdest, jmpath) for file in jmfiles]),
                              total=len(jmfiles), bar_format='{l_bar}{bar:20}{r_bar}{bar:-20b}'):
                    pass


def mergeLayers(tuple_in):
    """ Merges images by overlaying """
    file, jmdest, jmpath = tuple_in
    # Check if filename is valid
    if not re.match(r"^[\-0-9]*,[\-0-9]*.png$", file):
        return 0
    if os.path.exists(f"{jmdest}/{file}"):
        try:
            srcim = Image.open(f"{jmpath}/{file}")
            destim = Image.open(f"{jmdest}/{file}")
            destim.paste(srcim, (0, 0), srcim)
            destim.save(f"{jmdest}/{file}")
        except:
            print(f"File {jmpath}/{file} and/or {jmdest}/{file} is corrupted!")
    else:
        shutil.copyfile(f"{jmpath}/{file}", f"{jmdest}/{file}")
    return 1


def generateZooms(folder, level):
    """ Generate zoom 'level' PNGs based on a one unit smaller level """
    os.mkdir(f"{folder}/" + level)
    prevfolder = f"{folder}/" + str(int(level) + 1)
    toProcess = os.listdir(prevfolder)
    toProcessLen = len(toProcess)

    with tqdm(total=toProcessLen, bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}') as pbar:
        while len(toProcess) > 0:
            currentpic = toProcess[0]
            coords = [math.floor(int(currentpic.split(",")[0]) / 2),
                      math.floor(int(currentpic.split(",")[1].split(".")[0]) / 2)]
            newpic = Image.new('RGBA', (1024, 1024))
            for x in range(2):
                for z in range(2):
                    try:
                        nextpic = f"{coords[0] * 2 + x},{coords[1] * 2 + z}.png"
                        toProcess.remove(nextpic)
                    except ValueError:
                        continue  # File doesn't exist - ignore and continue
                    newpic.paste(Image.open(prevfolder + "/" + nextpic), (x * 512, z * 512))
            newpic = newpic.resize((512, 512))
            newpic.save(f"{folder}/{level}/{coords[0]},{coords[1]}.png")
            pbar.n = toProcessLen - len(toProcess)
            pbar.total = toProcessLen
            pbar.refresh()


def main():
    print("Journeymap to Coordman tiles converter")
    print("Note: This program may take a while to run")
    print("Please insert the full path to your Journeymap images folder "
          "(eg C:\\Users\\Popstonia\\AppData\\Roaming\\.minecraft\\journeymap\\data\\mp\\2b2t\\):")
    jmpath = input()

    if os.path.isdir("tiles/"):
        print("clearing tiles folder")
        shutil.rmtree("tiles/")
    os.mkdir("tiles")

    for dim in dimensions:
        print(f"Copying files for dimension {dim}...")
        generateMap(f"{jmpath}/{dim}", f"tiles/{dim}/0", dim)

    for level in range(levelcount):
        print(f"Generating level ({level + 1}/{levelcount}) for 3 dimensions...")
        pool = mp.Pool(3)
        pool.starmap(generateZooms, [(f"tiles/{dim}", "-" + str(level + 1)) for dim in dimensions])


if __name__ == '__main__':
    main()
