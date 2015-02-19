import os
import json
from copy import deepcopy #used to save contents of original file after modification

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

def ModifyFile(filename, newContents):
	changes = {'additions' : [], 'removals' : [], 'modifications': {}}
	old = {}
	with open(fullFile(filename), "r") as f:
		contents = json.load(f)
	old = deepcopy(contents)
	for newitem in newContents:
		if newitem in contents:
			# New item already exists in file
			if newContents[newitem] == None:
				# Already exists, deleting
				oldvalue = contents.pop(newitem)
				changes['removals'].append({newitem : oldvalue})
			else:
				# Already exists, just modifying, not deleting
				oldvalue = contents[newitem]
				contents[newitem] = newContents[newitem]
				changes['modifications'][newitem] = {"old_value" : oldvalue, "new_value" : newContents[newitem]}
		else:
			# New item doesn't exist yet, creating it
			if newContents[newitem] == None:
				# Skip the item completely, as it is null
				continue
			contents[newitem] = newContents[newitem]
			changes['additions'].append({newitem : newContents[newitem]})
	with open(fullFile(filename), "w+") as f:
		json.dump(contents, f)
	return {"old_contents" : old, "new_contents" : contents, "changes" : changes}