from misc import customErrors
import json
import random
import os
import gpt_2_simple as gpt2
from misc import WebSearch
from FilterParamsInference import PrologManager

class FilterParams:
    keywords =[]
    posFactor = None
    nchars = -1
    number_of_responses = 10
    slangFactor = None

    params = ["keywords", "posFactor", "nchars", "number_of_responses", "slangFactor"]

    def toString(self):
        kw = ""
        pf = ""
        nchars = ""
        nor = ""
        sf = ""
        ret = ""

        if not (self.posFactor is None):
            pf = f"-pf {self.posFactor}"
            ret = f"{pf} {ret}"

        if (self.nchars != -1):
            nchars = f"-nc {self.nchars}"
            ret = f"{nchars} {ret}"

        nor = f"-nor {self.number_of_responses}"
        ret = f"{nor} {ret}"

        if (len(self.keywords)):
            kw = "-k "
            for w in range(len(self.keywords) - 1):
                kw += str(self.keywords[w]) + ','
            kw += str(self.keywords[len(self.keywords) - 1])
            ret = f"{kw} {ret}"

        if not (self.slangFactor is None):
            sf = f"-sf {self.slangFactor}"
            ret = f"{sf} {ret}"

        return ret.rstrip()






default_model = "124M"
default_num_iterations = 5

def cprint(text):
    try:
        print(text)
        with open("log.txt","a") as f:
            f.write(f"{text}\n")
    except Exception as e:
        msg = f"Error in cprint: {str(e)}"
        print(msg)
        with open("log.txt", "a") as f:
            f.write(f"{msg}\n")


def checkFile(path): #checks if the file is available, throws exception otherwise
    try:
        t = open(path)
        t.close()
    except FileNotFoundError as e:
        raise FileNotFoundError("Path doesn't represent an available file:" + str(e))

def checkDir(path):
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Path doesn't represent a valid directory")


def checkAlphanumeric(inpt, *extrachars):
    for c in inpt:
        minuscula = (ord(c) >= ord('a') and ord(c) <= ord('z'))
        mayuscula = not minuscula and (ord(c) >= ord('A') and ord(c) <= ord('Z'))
        number = not mayuscula and (ord(c)>= ord('0') and ord(c) <= ord('9'))
        if(not minuscula and not mayuscula and not number and (c not in extrachars)):
            raise customErrors.InvalidCharsError("Not alphanumeric or in extrachars")

    return True

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

def checkModelExists(name):
    if not os.path.isdir(os.path.join("models", name)):
        raise customErrors.BadParamError("Model dir doesnt exists")

def uppercase(c):
    return ord(c) >= ord('A') and ord(c) <= ord('Z')

def error(msg):
    cprint(msg)
    raise customErrors.FatalError(msg)


def decModelDescriptor(md): #devuelve diccionario con elementos
    ret = {}
    out = json.loads(md)
    ret["name"] = out["name"]
    ret["keywords"] = out["keywords"]

    return ret


def fusionParams(p1,p2):
    ret = p1
    for p in FilterParams.params:
        if(eval(f"FilterParams.{p} != p2.{p}")):
            if(eval(f"FilterParams.{p} == p1.{p}")):
                exec(f"ret.{p} = p2.{p}")
    return ret.toString()


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
        elif (vec[i] == "-sf"):
            i += 1
            try:
                checkFloat(vec[i])
            except customErrors.InvalidCharsError as e:
                error("bad param: slangFactor" + " - " + str(e))
            ret.slangFactor = float(vec[i])
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

def textToAscii(text):
    out = ""
    c= 0
    while c < len(text):
        try:
            out += ' ' + str(ord(text[c]))
        except IndexError:
            pass
        c+=1
    return out.lstrip()

def asciiToText(text):
    out = ""
    v = text.split(" ")
    for c in v:
        out += chr(int(c))
    return out

def setupBaseModel(model = default_model):
    if not os.path.isdir(os.path.join("models", model)):
        cprint(f"Downloading {model} model...")
        gpt2.download_gpt2(model_name=model)
        cprint(f"model has been saved into current directory under /models/{model}/") # model is saved into current directory under /models/(model)/
    else:
        cprint(f'Model already installed, manually delete dir \"{model}\" if you want to reinstall this model')

def unifyWord(word, format_out = True):
    ret = WebSearch.request(f"{word} wikipedia").header
    if(ret == ""):
        ret = word
    if format_out:
        return PrologManager.formatText(ret)
    return ret