import os
import json

FILE_SUBDIR = "./files/"

def GetAllFiles():
	files = []
	for f in os.listdir(FILE_SUBDIR):
		if f.endswith(".json"):
			files.append(f)
	return files

def DoesFileExist(filename):
	files = GetAllFiles()
	for f in files:
		if f == filename:
			return True
	return False

def GetFile(filename):
	with open(FILE_SUBDIR + filename, "r") as f:
		contents = f.read()
	return json.loads(contents)