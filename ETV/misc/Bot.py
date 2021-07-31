from misc import customErrors, utils
from response_generation import responseGeneration
import json
from sentiment_analysis import sentimentAnalysis
from FilterParamsInference import Inferencer


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


class BotInstance:

    # PRIVATE

    def _getModelBasedOnContext(self, context):
        pass #TODO

    name = "noname"
    likes = []
    dislikes = []
    mymodels = []

    # PUBLIC

    def __init__(self, name, loadModels=[], likes=[], dislikes=[]):
        self.name = name
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

    def learn(self, model):
        self.mymodels.append(model)

    def toJSON(self):
        jsonFile = {"name": self.name, "mymodelsnames": self.mymodels, "likes": self.likes, "dislikes": self.dislikes}
        return json.dumps(jsonFile)


def jsonConstructor(inpt):
    try:
        out = json.loads(inpt)
        name = out["name"]
        modelsList = out["mymodels"]
        likes = out["likes"]
        dislikes = out["dislikes"]
    except Exception as e:
        raise customErrors.BadParamError("Bad JSON constructor: " + str(e))
    return BotInstance(name, modelsList, likes, dislikes)
