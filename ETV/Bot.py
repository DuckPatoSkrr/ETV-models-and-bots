import responseGeneration
import models
import json

class BotInstance:

    #PRIVATE

    def _punt(self, modelK, inputK):
        ret = 0
        for m in inputK:
            if(m in modelK):
                ret += 1
        return ret

    def _getModelBasedOnMood(self, keyw):
        max = 0
        ret = None
        for m in self.mymodelsnames:
            points = self._punt(self.modelKeywords[m], keyw)
            if(points > max):
                ret = m
                max = points

        return ret


    name = "noname"
    mymodelsnames = []
    modelKeywords = {}

    #PUBLIC

    def __init__(self, name, loadModels=[], modelKeywords={}):
        self.name = name
        self.mymodelsnames = loadModels
        self.modelKeywords = modelKeywords


    def generateResponse(self, modelKeywords, positivityFactor, msgKeywords,
                         prefix=None):
        model = self._getModelBasedOnMood(modelKeywords)
        return responseGeneration.generateResponse(model, positivityFactor, msgKeywords, prefix)


    def learn(self, corpusPath, nameOfModel,keywords):
        models.trainModel(corpusPath,nameOfModel)
        self.mymodelsnames.append(nameOfModel)
        self.modelKeywords[nameOfModel] = keywords

    def toJSON(self):
        jsonFile = {"name":self.name,"mymodelsnames":self.mymodelsnames,"modelKeywords":self.modelKeywords}
        return json.dumps(jsonFile)

def jsonConstructor(input):
    out = json.loads(input)
    name = out["name"]
    modelsList = out["mymodelsnames"]
    modelKw = out["modelKeywords"]
    return BotInstance(name,modelsList,modelKw)