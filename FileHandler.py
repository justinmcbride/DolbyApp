import os

FILE_SUBDIR = "./files/"

def GetAllFiles():
	files = []
	for f in os.listdir(FILE_SUBDIR):
		if f.endswith(".json"):
			files.append(f)
	return files