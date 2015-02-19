import os
import json

FILE_SUBDIR = "./files/"

def fullFile(filename):
	return FILE_SUBDIR + filename

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
	with open(fullFile(filename), "r") as f:
		contents = f.read()
	return json.loads(contents)

def DeleteFile(filename):
	os.remove(fullFile(filename))

def CreateFile(filename, contents):
	with open(fullFile(filename), "w") as f:
		f.write(json.dumps(contents))