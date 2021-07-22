from misc import customErrors
import json
import random

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
    try:
        float(n)
    except ValueError:
        raise customErrors.InvalidCharsError("Not a float")


def checkInt(n):
    try:
        int(n)
    except ValueError:
        raise customErrors.InvalidCharsError("Not a int")

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
    nchars = -1
    number_of_responses = 10


def filterParams(vec, pos): #devuelve objeto FilterParams
    ret = FilterParams()
    i = pos
    while i in range(pos,len(vec)):
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
            ret.posFactor = float(vec[i])
        elif(vec[i] == "-nc"):
            i += 1
            try:
                checkInt(vec[i])
            except customErrors.InvalidCharsError as e:
                error("bad param: max number of chars" + " - " + str(e))
            ret.nchars = int(vec[i])
        elif(vec[i] == "-nor"):
            i += 1
            try:
                checkInt(vec[i])
            except customErrors.InvalidCharsError as e:
                error("bad param: number of responses" + " - " + str(e))
            ret.number_of_responses = int(vec[i])
        else:
            error("unknown param: " + str(vec[i]))
        i += 1

    return ret


def copyList(src,dest):
    for i in src:
        dest.append(i)
    return dest

def getRandomInt(a = 0,b=None):
    if(b is None):
        return int(random.random())

    return random.randint(a,b)

def removeChars(text, *chars, char=" "):
    for i in chars:
        text = text.replace(chr(ord(i)),chr(ord(char)))
    return text

def literalQuotes(text):
    out = ""
    for c in text:
        if(ord(c) == 34):
            out += chr(92) + chr(34)
        else:
            out += c
    return out