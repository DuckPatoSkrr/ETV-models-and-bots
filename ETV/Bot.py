import responseGeneration
import json
import sentimentAnalysis
import utils


def _punt(modelK, inputK):
    ret = 0
    for m in inputK:
        if(m in modelK):
            ret += 1
    return ret
def _extractKWfromContext(context): #devuelve lista
    classifier = sentimentAnalysis.Classifier()
    prop = classifier.classify(context)
    ret = []
    ret = utils.copyList(prop.pnouns,ret)
    ret = utils.copyList(prop.adjectives,ret)
    return ret

class BotInstance:

    #PRIVATE

    def _getModelBasedOnMood(self, keyw):
        maxn = 0
        ret = None
        for m in self.mymodelsnames:
            points = _punt(self.modelKeywords[m], keyw)
            if(points > maxn):
                ret = m
                maxn = points

        return ret

    name = "noname"
    mymodelsnames = []
    modelKeywords = {}

    #PUBLIC

    def __init__(self, name, loadModels=[], modelKeywords={}):
        self.name = name
        self.mymodelsnames = loadModels
        self.modelKeywords = modelKeywords

    def generateResponse(self, context, filterParams,
                         prefix=None):
        modelKeywords = _extractKWfromContext(context)
        model = self._getModelBasedOnMood(modelKeywords)
        return responseGeneration.generateResponse(model, filterParams.posFactor, filterParams.keywords,
                                                   prefix)


    def learn(self, nameOfModel,keywords):
        self.mymodelsnames.append(nameOfModel)
        self.modelKeywords[nameOfModel] = keywords

    def toJSON(self):
        jsonFile = {"name":self.name,"mymodelsnames":self.mymodelsnames,"modelKeywords":self.modelKeywords}
        return json.dumps(jsonFile)

def jsonConstructor(inpt):
    out = json.loads(inpt)
    name = out["name"]
    modelsList = out["mymodelsnames"]
    modelKw = out["modelKeywords"]
    return BotInstance(name,modelsList,modelKw)