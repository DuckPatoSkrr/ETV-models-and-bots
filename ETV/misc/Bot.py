import pyswip.prolog

from misc import customErrors, utils
from response_generation import responseGeneration
import json
from sentiment_analysis import sentimentAnalysis
from FilterParamsInference import Inferencer,PrologManager
from models import models
from misc import WebSearch

learn_threshold = 0

def _punt(modelK, inputK):

    words2compare = []
    for sentence in inputK:
        words2compare += sentence.pnouns
        words2compare += sentence.nouns

    res = 0
    for w in words2compare:
        res += _relation(modelK, utils.unifyWord(w))

    return res / (len(words2compare) * len(modelK))


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
        try:
            res = man.consult(f"show_r({PrologManager.formatText(i)},{PrologManager.formatText(word)},P)")
            ret += abs(res["P"])
        except pyswip.prolog.PrologError as e:
            utils.cprint(f"PROLOG ERROR: {str(e)}")
    return ret


class BotInstance:

    # PRIVATE

    def _getModelBasedOnContext(self, context):
        maxp = -1
        ret = None
        cl = sentimentAnalysis.Classifier()
        prop = cl.classify(context)
        for m in self.mymodels:
            model = models.jsonConstructor(m)
            p = _punt(model.keywords, prop)
            if(p > maxp):
                ret = model
                maxp = p
        if(ret is None):
            ret = models.jsonConstructor(self.mymodels[0])
            utils.cprint("Selected random model.")
        return ret

    def _modelFits(self,model):
        punt = 0
        total = (len(self.likes) + len(self.dislikes)) * len(model.keywords)
        for kw in model.keywords:
            punt += _relation(self.likes,kw)
            punt += _relation(self.dislikes,kw)

        return (punt / total) >= learn_threshold



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

        if not self.mymodels:
            utils.error("Cant generate response, untrained bot.")

        utils.cprint(f"Generating response, params recived: {filterParams.toString()}")

        inferedParams = Inferencer.inferParams(self, context)
        finalParams = utils.fusionParams(filterParams, inferedParams)
        finalParams = utils.filterParams(finalParams.split(" "), 0)

        model = self._getModelBasedOnContext(context)
        return responseGeneration.generateResponse(model, finalParams.posFactor, finalParams.keywords,
                                                   finalParams.nchars,
                                                   finalParams.number_of_responses, finalParams.slangFactor,
                                                   prefix=context)

    def learn(self, modelList):
        for m in modelList:
            model = models.jsonConstructor(m)
            if(self._modelFits(model)):
                self.mymodels.append(model.toJSON())

    def toJSON(self):
        jsonFile = {"age": self.age, "level_of_education":self.level_of_education, "mymodelsnames": self.mymodels, "likes": self.likes, "dislikes": self.dislikes}
        return json.dumps(jsonFile)


def jsonConstructor(inpt):
    try:
        out = json.loads(inpt)
        age = out["age"]
        level_of_education = out["level_of_education"]
        modelsList = out["mymodelsnames"]
        likes = out["likes"]
        dislikes = out["dislikes"]
    except Exception as e:
            raise customErrors.BadParamError("Bad JSON constructor: " + str(e))
    return BotInstance(age,level_of_education, modelsList, likes, dislikes)
