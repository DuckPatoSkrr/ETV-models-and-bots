import customErrors
import json

def checkFile(path): #checks if the file is available, throws exception otherwise
    try:
        t = open(path)
        t.close()
    except FileNotFoundError:
        raise FileNotFoundError("Path doesn't represent an available file")

def checkAlphanumeric(inpt, *extrachars):
    for c in inpt:
        minuscula = (ord(c) >= ord('a') and ord(c) <= ord('z'))
        mayuscula = not minuscula and (ord(c) >= ord('A') and ord(c) <= ord('Z'))
        number = not mayuscula and (ord(c)>= ord('0') and ord(c) <= ord('9'))
        if(not minuscula and not mayuscula and not number and (c not in extrachars)):
            raise customErrors.InvalidCharsError("Not alphanumeric or in extrachars")

def checkFloat(n):
    if not isinstance(n,float):
        raise customErrors.InvalidCharsError("Not a float")

def error(msg):
    raise customErrors.FatalError(msg)

def modelDescriptor(name,kw):
    jsonFile = {"name": name, "keywords": kw}
    return json.dumps(jsonFile)

def decModelDescriptor(md): #devuelve diccionario con elementos
    ret = {}
    out = json.loads(md)
    ret["name"] = out["name"]
    ret["keywords"] = out["keywords"]

    return ret


class FilterParams:
    keywords =[]
    posFactor = None


#-k keyword1,keyword2
#-pf float
def filterParams(vec, pos): #devuelve objeto FilterParams
    ret = FilterParams()
    for i in range(pos,len(vec)):
        if(vec[i] == "-k"):
            i += 1
            try:
                checkAlphanumeric(vec[i],",")
            except customErrors.InvalidCharsError as e:
                error("bad param: keywords"+ " - " + str(e))
            ret.keywords = vec[i].split(",")
        elif(vec[i] == "-pf"):
            i+= 1
            try:
                checkFloat(vec[i])
            except customErrors.InvalidCharsError as e:
                error("bad param: posFactor" + " - " + str(e))
            ret.posFactor = vec[i]
        else:
            error("unknown param: " + vec[i])

    return ret