

def checkFile(path): #checks if the file is available, throws exception otherwise
    try:
        t = open(path)
        t.close()
    except:
        raise FileNotFoundError("Path doesn't represent an available file")