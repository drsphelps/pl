import os, sys
# TODO: Need to implement mp3 reading
import mutagen

def readFilesFromDisk(rootDir):
    for dirName, subdirList, fileList in os.walk(rootDir):
        for file in fileList:
            if '.mp3' in file:
    		filePath = os.path.join(os.path.abspath(dirName), file)
    		filePath = filePath.replace(" ", "\ ")
    		print(filePath)
