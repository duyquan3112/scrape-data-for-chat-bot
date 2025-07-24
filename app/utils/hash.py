import hashlib
import json
import os

hashesPath = "data/hashed_data.json"

def getHash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def loadHashes(path=hashesPath):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def saveHashes(hashes, path=hashesPath):
    with open(path, 'w') as f:
        json.dump(hashes, f)