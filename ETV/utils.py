import customErrors

def checkFile(path): #checks if the file is available, throws exception otherwise
    try:
        t = open(path)
        t.close()
    except:
        raise FileNotFoundError("Path doesn't represent an available file")

def checkAlphanumeric(input, *extrachars):
    for c in input:
        minuscula = (ord(c) >= ord('a') and ord(c) <= ord('z'))
        mayuscula = (ord(c) >= ord('A') and ord(c) <= ord('Z'))
        if(not minuscula and not mayuscula and (c not in extrachars)):
            raise customErrors.InvalidCharsError("Not alphanumeric or in extrachars")


def error(msg):
    pass#TODO

def filterParams():
    pass#TODO

def modelDescriptor(name,kw):
    pass#TODO

def decModelDescriptor(md): #devuelve diccionario con elementos
    pass #TODO

def filterParams(vec, pos): #devuelve diccionario
    pass #TODO