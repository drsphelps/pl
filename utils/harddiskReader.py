import os, sys

rootDir = sys.argv[1]
print(sys.argv)
for dirName, subdirList, fileList in os.walk(rootDir):
    for file in fileList:
        if '.mp3' in file:
		filePath = os.path.join(os.path.abspath(dirName), file)
		filePath = filePath.replace(" ", "\ ")
		print(filePath)

