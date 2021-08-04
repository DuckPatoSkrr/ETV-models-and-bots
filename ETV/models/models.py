import os
import gpt_2_simple as gpt2
from misc import utils
import json
from misc import customErrors
from misc.wordCounter import wordCounter
from shutil import copyfile
models_dir = "models"
default_model_version = "124M"

# PRIVATE

corpus_dir = "./rawCorpus/"

def _generateKeywords(path,n=100):
    ret =[]
    name = path.split("/")[len(path.split("/")) - 1]
    nameout = f"{name}out"
    utils.cprint("Extracting keywords from corpus...")

    #Tokenize text
    wordCounter.tokenize(path, f"{corpus_dir}tokenizedRawCorpus/{name}")

    #Counting words
    copyfile(f"{corpus_dir}tokenizedRawCorpus/{name}", f"./misc/wordCounter/{name}")
    wordCounter.counter(name, nameout, n)

    with open(f"./misc/wordCounter/{nameout}") as f:
        for line in f:
            ret.append(line.rstrip("\n"))

    os.remove(f"./misc/wordCounter/{name}")
    os.remove(f"./misc/wordCounter/{nameout}")

    return ret

#PUBLIC

def appendModelDescriptorList(mdl, model):
    mdl.append(model.toJSON())
    return mdl

def getModelDescriptorListObj(mdl):
    try:
        ret = json.loads(mdl)["list"]
    except json.JSONDecodeError:
        ret = []
    return ret

def modelDescriptorListToJSON(mdl):
    jsonFile = {"list":mdl}
    return json.dumps(jsonFile)

def jsonConstructor(jsonin):
    try:
        out = json.loads(jsonin)
        name = out["name"]
        kw = out["keywords"]
        path = out["path"]
    except Exception as e:
        raise customErrors.BadParamError("Bad JSON constructor: " + str(e))
    return Model(name,corpusPath=path, keywords=kw)

class Model:
    name = ""
    keywords = []
    path = ""

    def __init__(self,name,corpusPath=None,num_iterations=0,keywords=[]):
        if num_iterations > 0 and not (corpusPath is None):
            trainModel(corpusPath,name,num_iterations)
        self.name = name

        if len(keywords) != 0:
            self.keywords = keywords
        elif not (corpusPath is None):
            self.keywords = _generateKeywords(corpusPath)
        self.path = corpusPath


    def toJSON(self):
        jsonFile = {"name": self.name, "keywords": self.keywords, "path":self.path}
        return json.dumps(jsonFile)

#corpus must be a txt
def trainModel(corpusPath, nameOfModel, num_iterations = 5, _model_version = default_model_version): #124M o 355M
    if not os.path.isdir(os.path.join(models_dir, _model_version)):
        utils.error("Base model introduced does not exist in specified dir")

    utils.checkFile(corpusPath)

    sess = gpt2.start_tf_sess() #config (threads and external server)
    gpt2.finetune(sess, corpusPath,
                  model_name=_model_version, steps=num_iterations, run_name=nameOfModel,
                  restore_from='fresh', multi_gpu=False,)  # steps is max number of training step