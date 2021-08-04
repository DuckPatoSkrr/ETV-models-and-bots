from misc import customErrors, utils
from response_generation import responseGeneration
import json
from sentiment_analysis import sentimentAnalysis
from FilterParamsInference import Inferencer,PrologManager
from models import models
from misc import WebSearch

learn_threshold = 0

def _punt(modelK, inputK):
    ret = 0
    for m in inputK:
        if (m in modelK):
            ret += 1
    return ret


def _extractKWfromContext(context):  # devuelve lista
    classifier = sentimentAnalysis.Classifier()
    prop = classifier.classify(context)
    ret = []
    ret = utils.copyList(prop.pnouns, ret)
    ret = utils.copyList(prop.adjectives, ret)
    return ret

def _relation(likes, word):
    ret = 0
    man = PrologManager.Manager()

    for i in likes:
        iunified = WebSearch.request(f"{i} wikipedia").header
        wordunified = WebSearch.request(f"{word} wikipedia").header
        res = man.consult(f"show_r({PrologManager.formatText(i)},{PrologManager.formatText(wordunified)},P)")
        ret += abs(res["P"])
    return ret


class BotInstance:

    # PRIVATE

    def _getModelBasedOnContext(self, context): #TODO igual esto se puede hacer mejor
        maxp = -1
        for m in self.mymodels:
            p = _punt(m.keywords, context)
            if(p > maxp):
                ret = m
                maxp = p
        return ret

    def _modelFits(self,model):
        punt = 0
        for kw in model.keywords:
            punt += _relation(self.likes,kw)
            punt += _relation(self.dislikes,kw)

        return punt >= learn_threshold



    age = None
    level_of_education = None
    likes = []
    dislikes = []
    mymodels = []

    # PUBLIC

    def __init__(self, age, level_of_education, loadModels=[], likes=[], dislikes=[]):
        self.age = age
        self.level_of_education = level_of_education
        self.mymodels = loadModels
        self.likes = likes
        self.dislikes = dislikes

    def generateResponse(self, context, filterParams,
                         prefix=None):

        inferedParams = Inferencer.inferParams(self, context)
        finalParams = utils.fusionParams(filterParams, inferedParams)
        finalParams = utils.filterParams(finalParams.split(" "), 0)

        model = self._getModelBasedOnContext(context)
        return responseGeneration.generateResponse(model, finalParams.posFactor, finalParams.keywords,
                                                   finalParams.nchars,
                                                   finalParams.number_of_responses,
                                                   prefix)

    def learn(self, modelList):
        for m in modelList:
            model = models.jsonConstructor(m)
            if(self._modelFits(model)):
                self.mymodels.append(model)

    def toJSON(self):
        jsonFile = {"age": self.age, "level_of_education":self.level_of_education, "mymodelsnames": self.mymodels, "likes": self.likes, "dislikes": self.dislikes}
        return json.dumps(jsonFile)


def jsonConstructor(inpt):
    try:
        out = json.loads(inpt)
        age = out["age"]
        level_of_education = out["level_of_education"]
        modelsList = out["mymodels"]
        likes = out["likes"]
        dislikes = out["dislikes"]
    except Exception as e:
        raise customErrors.BadParamError("Bad JSON constructor: " + str(e))
    return BotInstance(age,level_of_education, modelsList, likes, dislikes)
